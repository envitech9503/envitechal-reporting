#!/bin/bash
# Envi Tech AL - pull deployment v2 (owner decision 24-10-2026, option 1; strict-QA fixes of 23-10-2026).
# Runs every 5 minutes (etal-autodeploy.timer). Deploys the newest git tag named deploy-YYYYMMDD-HHMM pushed to
# GitHub (origin) when it is a fast-forward of the running code:
#   backup (pg_dump) -> merge -> check -> migrate -> collectstatic (only if static/ changed) -> reload -> health check.
# On a failure the code is put back and gunicorn reloaded (restarted if it is down). An interrupted deployment is
# detected on the next run through the in-flight marker and completed or rolled back - it is never reported "ok"
# without migrate + reload. Result: /var/log/etal-deploy.log and a GitHub tag status/<tag>-ok|-failed (retried
# until pushed). Requirements changes are never installed automatically (failed: manual deployment).
set -u
APP=/home/django/EnviTechAlApp
STATE=/var/lib/etal-deploy
LOG=/var/log/etal-deploy.log
BK=/var/backups/etal-deploy
LIB=/usr/local/lib/etal-deploy
MENV=/root/bin/menvd.py
MAX_BACKUP_TRIES=3
MIN_FREE_KB=1500000            # pg_dump needs about 250 MB; keep at least 1.5 GB free
exec 9>/run/etal-deploy.lock
flock -n 9 || exit 0
mkdir -p "$STATE"; install -d -o django -g www-data -m 750 "$BK"
log() { echo "$(date '+%d-%m-%Y %H:%M:%S') $*" >> "$LOG"; }
G() { sudo -u django git -C "$APP" "$@"; }
gpid() { local p; p=$(systemctl show -p MainPID --value gunicorn 2>/dev/null); [ -n "$p" ] && [ "$p" != "0" ] && echo "$p"; }
reload() {   # graceful reload; a stopped/crashed gunicorn is restarted instead
  local p; p=$(gpid)
  if [ -n "$p" ]; then kill -HUP "$p"; else log "gunicorn not running - systemctl restart"; systemctl restart gunicorn; fi
  sleep 10
}
health() {
  curl -s -o /dev/null -w '%{http_code}' --max-time 30 --unix-socket /run/gunicorn.sock \
    -H 'Host: report.envitechal.com' -H 'X-Forwarded-Proto: https' -H 'X-Real-IP: 110.93.247.168' http://localhost/login/
}
healthy() { local h; h=$(health); [ "$h" = "200" ] && return 0; sleep 10; h=$(health); [ "$h" = "200" ]; }
menv() {     # run a helper as the django user with the gunicorn environment (needs a running master)
  local p; p=$(gpid)
  if [ -z "$p" ]; then systemctl restart gunicorn; sleep 8; p=$(gpid); fi
  [ -n "$p" ] || { log "gunicorn is not running - cannot run $1"; return 1; }
  python3 "$MENV" "$p" "$@" >> "$LOG" 2>&1
}
push_status() {   # $1 tag  $2 ok|failed  $3 commit ; retried on later runs until GitHub has it
  local t="status/$1-$2"
  if G tag -f "$t" "$3" >/dev/null 2>&1 && G push -q -f origin "refs/tags/$t" >> "$LOG" 2>&1; then
    rm -f "$STATE/pending_$1"
  else
    echo "$2 $3" > "$STATE/pending_$1"; log "$1: status tag push failed - will retry"
  fi
}
finish() {   # $1 ok|failed  $2 commit
  touch "$STATE/done_$TAG"; rm -f "$STATE/inflight" "$STATE/tries_$TAG"
  push_status "$TAG" "$1" "$2"
}
rollback() { # $1 reason ; code back to $OLD, reload, status failed
  G reset -q --hard "$OLD"; reload
  local h; h=$(health)
  if [ "$h" != "200" ]; then log "$TAG: health $h after rollback - systemctl restart gunicorn"; systemctl restart gunicorn; sleep 10; h=$(health); fi
  log "$TAG: FAILED - $1; code put back to $OLD and reloaded (health $h); database backup $BK/$TAG.dump; migrations already applied stay applied"
  finish failed "$NEW"
}

# 0) status tags that could not be pushed earlier
for f in "$STATE"/pending_*; do
  [ -e "$f" ] || continue
  t=${f##*/pending_}; read -r st cm < "$f"; push_status "$t" "$st" "$cm"
done

# 1) an interrupted deployment (reboot, timeout, kill) is completed or rolled back first
if [ -f "$STATE/inflight" ]; then
  read -r TAG OLD NEW STATIC < "$STATE/inflight"
  log "$TAG: resuming an interrupted deployment ($OLD -> $NEW)"
  if [ "$(G rev-parse HEAD)" != "$NEW" ]; then
    G reset -q --hard "$OLD"; reload; log "$TAG: interrupted before the merge finished - code left at $OLD; will retry"; rm -f "$STATE/inflight"; exit 0
  fi
  if ! menv "$LIB/etal_migrate.py" "$STATIC"; then rollback "check/migrate (after interruption)"; exit 0; fi
  reload
  if healthy; then log "$TAG: DEPLOYED $NEW after resuming (health 200)"; G push -q origin HEAD:main >> "$LOG" 2>&1; finish ok "$NEW"
  else rollback "health check after resuming"; fi
  exit 0
fi

# 2) the newest well-formed deploy tag (names sort by date and time)
G fetch -q --tags --force --prune-tags origin 2>>"$LOG" || { log "fetch failed"; exit 0; }
TAG=$(G tag -l 'deploy-*' | grep -E '^deploy-[0-9]{8}-[0-9]{4}$' | sort -r | head -1)
[ -z "$TAG" ] && exit 0
[ -f "$STATE/done_$TAG" ] && exit 0
NEW=$(G rev-parse "$TAG^{commit}"); OLD=$(G rev-parse HEAD)
log "$TAG: start ($OLD -> $NEW)"
if [ "$NEW" = "$OLD" ] || G merge-base --is-ancestor "$NEW" "$OLD"; then
  log "$TAG: already contained in the running code"; finish ok "$NEW"; exit 0; fi
if ! G merge-base --is-ancestor "$OLD" "$NEW"; then log "$TAG: FAILED - not a fast-forward of the running code"; finish failed "$NEW"; exit 0; fi
if [ -n "$(G status --porcelain --untracked-files=no)" ]; then log "$TAG: FAILED - production working tree has local changes"; finish failed "$NEW"; exit 0; fi
CHANGED=$(G diff --name-only "$OLD" "$NEW")
if echo "$CHANGED" | grep -q -i '^requirements'; then log "$TAG: FAILED - requirements changed, manual deployment needed"; finish failed "$NEW"; exit 0; fi

# 3) backup (limited retries; disk space checked; a partial dump is removed)
FREE=$(df -Pk "$BK" | awk 'NR==2{print $4}')
TRIES=$(cat "$STATE/tries_$TAG" 2>/dev/null || echo 0)
if [ "${FREE:-0}" -lt "$MIN_FREE_KB" ] || ! menv "$LIB/etal_backup.py" "$BK/$TAG.dump"; then
  rm -f "$BK/$TAG.dump"; TRIES=$((TRIES + 1)); echo "$TRIES" > "$STATE/tries_$TAG"
  if [ "$TRIES" -ge "$MAX_BACKUP_TRIES" ]; then log "$TAG: FAILED - backup failed $TRIES times (free ${FREE:-?} KB)"; finish failed "$NEW"
  else log "$TAG: backup failed (attempt $TRIES of $MAX_BACKUP_TRIES, free ${FREE:-?} KB) - will retry"; fi
  exit 0
fi
ls -1t "$BK"/*.dump 2>/dev/null | tail -n +6 | xargs -r rm -f
log "$TAG: backup $BK/$TAG.dump ($(du -h "$BK/$TAG.dump" | cut -f1))"

# 4) deploy
STATIC=0; echo "$CHANGED" | grep -q '^static/' && STATIC=1
echo "$TAG $OLD $NEW $STATIC" > "$STATE/inflight"
if ! G merge --ff-only -q "$NEW" >> "$LOG" 2>&1; then G reset -q --hard "$OLD"; log "$TAG: FAILED - merge"; finish failed "$NEW"; exit 0; fi
if ! menv "$LIB/etal_migrate.py" "$STATIC"; then rollback "check/migrate"; exit 0; fi
reload
if ! healthy; then rollback "health check $(health) after reload"; exit 0; fi
G push -q origin HEAD:main >> "$LOG" 2>&1 || log "$TAG: note - push of main to GitHub failed"
log "$TAG: DEPLOYED $NEW (health 200)"
finish ok "$NEW"
