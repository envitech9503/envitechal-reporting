# Envi Tech AL – pull deployment (server files)

These files are installed on the droplet; this copy is kept in the repository for review and versioning only.

| File | Installed at |
|---|---|
| `etal-autodeploy.sh` | `/root/bin/etal-autodeploy.sh` (mode 700) |
| `etal_backup.py`, `etal_migrate.py` | `/usr/local/lib/etal-deploy/` (mode 644; run as the django user through `/root/bin/menvd.py`) |
| `etal-autodeploy.service`, `etal-autodeploy.timer` | `/etc/systemd/system/` (timer: every 5 minutes) |

## How to deploy

1. The owner approves the deployment.
2. Push a commit to `main` with a tag named `deploy-YYYYMMDD-HHMM`.
3. Within 5 minutes the server runs: backup, fast-forward, check, migrate, collectstatic (only if `static/` changed), graceful reload, health check.
4. The result is pushed as `status/<tag>-ok` or `status/<tag>-failed`. The log is `/var/log/etal-deploy.log`.

## Rollback and resume

- **Failed step:** the code is put back to the previous commit and gunicorn is reloaded. If gunicorn has stopped, it is restarted.
- **Interrupted run:** the in-flight marker makes the next run finish or roll back the deployment.
