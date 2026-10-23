"""Envi Tech AL pull deployment: database backup before a deployment (pg_dump custom format). The password is
passed to pg_dump through the environment and never printed."""
import os
import subprocess
import sys

sys.path.insert(0, os.getcwd()); os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EnviTechAlApp.settings')
import django  # noqa: E402
django.setup()
from django.conf import settings  # noqa: E402

db = settings.DATABASES['default']
out = sys.argv[1]
if 'postgresql' not in db['ENGINE']:
    print('backup: database is not PostgreSQL - skipped'); sys.exit(1)
env = dict(os.environ, PGPASSWORD=str(db.get('PASSWORD') or ''))
cmd = ['pg_dump', '-Fc', '-U', str(db['USER']), '-f', out, str(db['NAME'])]
if db.get('HOST'):                       # empty HOST = local socket (same as Django)
    cmd[2:2] = ['-h', str(db['HOST'])]
if db.get('PORT'):
    cmd[2:2] = ['-p', str(db['PORT'])]
r = subprocess.run(cmd, env=env, stderr=subprocess.PIPE)
if r.returncode != 0 or not os.path.exists(out) or os.path.getsize(out) < 1024:
    if os.path.exists(out):
        os.remove(out)
    print('backup failed: %s' % r.stderr.decode(errors='replace')[-300:]); sys.exit(1)
os.chmod(out, 0o640)
