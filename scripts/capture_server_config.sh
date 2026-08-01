#!/usr/bin/env bash
#
# Keep the server's own configuration in the repository.
#
#   sudo ./scripts/capture_server_config.sh            show what has drifted
#   sudo ./scripts/capture_server_config.sh --capture  copy the live files in
#   sudo ./scripts/capture_server_config.sh --install  push the repo copies out
#
# The nginx site file and the systemd units are as much a part of this system as
# the Python is - the TLS setup, the /static alias, the favicon rule and the
# one-year cache on hashed assets all live there. None of it was in version
# control, so rebuilding the droplet would have lost it silently.
#
# Files that contain a credential are never copied in. The database password is
# set through a systemd drop-in; that drop-in stays on the server only.
#
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")/.."

DEST=deploy/server
say()  { printf '\n\033[1;32m==>\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m  ! \033[0m%s\n' "$*"; }
die()  { printf '\n\033[1;31m==>\033[0m %s\n' "$*" >&2; exit 1; }

FILES=(
    /etc/nginx/sites-available/report.envitechal.com
    /etc/systemd/system/gunicorn.service
    /etc/systemd/system/gunicorn.socket
    /etc/systemd/system/django.service
)

MODE=diff
case "${1:-}" in
    --capture) MODE=capture ;;
    --install) MODE=install ;;
    ""|--diff) MODE=diff ;;
    *) die "unknown option: $1" ;;
esac

mkdir -p "$DEST"
drift=0

for src in "${FILES[@]}"; do
    name=$(basename "$src")
    repo="$DEST/$name"

    if [ ! -f "$src" ]; then
        warn "not present on this machine: $src"
        continue
    fi

    # Never pull a credential into the repository.
    if grep -qiE '(password|secret|api[_-]?key)[[:space:]]*=' "$src"; then
        warn "skipping $name - it contains a credential, keep it on the server only"
        continue
    fi

    case "$MODE" in
        capture)
            install -m 0644 "$src" "$repo"
            printf '  captured %s\n' "$name"
            ;;
        install)
            [ -f "$repo" ] || { warn "no repo copy of $name to install"; continue; }
            if cmp -s "$src" "$repo"; then
                printf '  unchanged %s\n' "$name"
            else
                cp -a "$src" "$src.$(date +%Y%m%d%H%M%S).bak"
                install -m 0644 "$repo" "$src"
                printf '  installed %s (previous version kept alongside it)\n' "$name"
            fi
            ;;
        diff)
            if [ ! -f "$repo" ]; then
                warn "$name is not in the repository yet - run with --capture"
                drift=1
            elif ! cmp -s "$src" "$repo"; then
                warn "$name on this server differs from the repository:"
                diff -u "$repo" "$src" | sed 's/^/      /' || true
                drift=1
            else
                printf '  in sync   %s\n' "$name"
            fi
            ;;
    esac
done

if [ "$MODE" = install ]; then
    say "Validating and reloading"
    nginx -t
    systemctl reload nginx
    systemctl daemon-reload
    printf '  nginx reloaded, systemd re-read\n'
fi

if [ "$MODE" = diff ] && [ "$drift" = 1 ]; then
    say "Server configuration has drifted from the repository."
    exit 1
fi

say "Done."
