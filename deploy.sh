#!/usr/bin/env bash
#
# Envi Tech AL — deploy the reporting portal.
#
#   sudo ./deploy.sh              pull, rebuild static assets, restart
#   sudo ./deploy.sh --migrate    ... and apply database migrations as well
#   sudo ./deploy.sh --no-pull    rebuild and restart what is already checked out
#
# Why this exists: nginx serves /static from staticfiles/, which collectstatic
# builds from static/. Editing a stylesheet or a script alone changes nothing
# that a visitor can see. Rebuilding used to be a separate step someone had to
# remember, and on 31-07-2026 it was forgotten twice in one evening. It is not a
# separate step any more.
#
set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")"

PY=venv/bin/python
[ -x "$PY" ] || PY=python3

say()  { printf '\n\033[1;32m==>\033[0m %s\n' "$*"; }
warn() { printf '\n\033[1;33m==>\033[0m %s\n' "$*"; }
die()  { printf '\n\033[1;31m==>\033[0m %s\n' "$*" >&2; exit 1; }

[ -f manage.py ] || die "manage.py not found - run this from the project directory."

DO_PULL=1
DO_MIGRATE=0
for arg in "$@"; do
    case "$arg" in
        --migrate) DO_MIGRATE=1 ;;
        --no-pull) DO_PULL=0 ;;
        *) die "unknown option: $arg" ;;
    esac
done

# ---------------------------------------------------------------- 1. source
if [ "$DO_PULL" = 1 ]; then
    say "Fetching latest code"
    git pull --ff-only
fi
say "Deploying $(git log --oneline -1)"

# ---------------------------------------------------------------- 2. checks
say "Checking the project"
$PY manage.py check
$PY scripts/check_templates.py

# ---------------------------------------------------------------- 3. static
# ManifestStaticFilesStorage rebuilds every asset with a content hash in its
# name, so browsers pick up changes the moment this runs. Old hashed files are
# deliberately left in place: a visitor holding a cached page can still fetch
# the assets that page refers to.
say "Rebuilding static assets"
$PY manage.py collectstatic --noinput | tail -3
if [ "$(id -u)" = 0 ]; then
    chown -R --reference=manage.py staticfiles
fi

# ---------------------------------------------------------------- 4. database
if [ "$DO_MIGRATE" = 1 ]; then
    # Without USE_POSTGRES=1 the settings fall back to a local sqlite file, so a
    # migration run here would quietly build a throwaway database instead of
    # touching the real one. Refuse rather than do that.
    #
    # The service reads its database settings from a systemd drop-in, so read the
    # same file rather than asking anyone to retype a password. Only the four
    # expected keys are taken, the values are never printed, and nothing is
    # eval'd - a password containing a space or a shell character is safe here.
    if [ "${USE_POSTGRES:-}" != "1" ]; then
        DROPIN=$(ls /etc/systemd/system/gunicorn.service.d/*.conf 2>/dev/null | head -1 || true)
        if [ -n "${DROPIN:-}" ] && [ -r "$DROPIN" ]; then
            while IFS= read -r line; do
                line=${line#Environment=}
                line=${line#\"}; line=${line%\"}
                key=${line%%=*}; val=${line#*=}
                case "$key" in
                    USE_POSTGRES|PG_NAME|PG_USER|PG_PASSWORD|PG_HOST|PG_PORT)
                        export "$key=$val" ;;
                esac
            done < <(grep '^Environment=' "$DROPIN" || true)
            printf '  read the database environment from %s\n' "$DROPIN"
        fi
    fi
    if [ "${USE_POSTGRES:-}" != "1" ]; then
        die "--migrate needs the PostgreSQL environment (USE_POSTGRES=1 and the PG_* variables).
    Without it Django falls back to sqlite and would migrate the wrong database.
    Expected them in a systemd drop-in under /etc/systemd/system/gunicorn.service.d/."
    fi
    say "Applying database migrations to PostgreSQL database ${PG_NAME:-django}"
    $PY manage.py migrate --noinput
else
    warn "Skipping migrations. If this release changes any model, run: sudo ./deploy.sh --migrate"
fi

# ---------------------------------------------------------------- 5. restart
say "Restarting services"
systemctl restart gunicorn
systemctl restart django
sleep 4
systemctl is-active gunicorn django

# ---------------------------------------------------------------- 6. smoke test
# Test the real path a visitor takes - TLS, nginx, gunicorn - by resolving the
# site's own hostname to this machine. A plain http://127.0.0.1 request answers
# from nginx's default server block (404) or gets redirected to https (301),
# neither of which tells you whether the site actually works.
say "Checking the site responds"
HOST=report.envitechal.com
probe() { curl -sS -o /dev/null --max-time 25 --resolve "$HOST:443:127.0.0.1" -w '%{http_code}' "https://$HOST$1" || echo 000; }

code=$(probe /login/)
[ "$code" = 200 ] || die "/login/ returned $code - check: journalctl -u gunicorn -n 50"
printf '    /login/ -> %s\n' "$code"

asset=$($PY - <<'PYEOF'
import json
print(json.load(open('staticfiles/staticfiles.json'))['paths']['js/app.js'])
PYEOF
)
code=$(probe "/static/$asset")
[ "$code" = 200 ] || die "hashed asset /static/$asset returned $code - check the nginx /static/ alias."
printf '    /static/%s -> %s\n' "$asset" "$code"

say "Deployed."
