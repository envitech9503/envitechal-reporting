"""Envi Tech AL pull deployment: system check, migrations and (when static files changed) collectstatic."""
import os
import sys

sys.path.insert(0, os.getcwd()); os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EnviTechAlApp.settings')
import django  # noqa: E402
django.setup()
from django.core.management import call_command  # noqa: E402

call_command('check')
call_command('migrate', interactive=False, verbosity=1)
if len(sys.argv) > 1 and sys.argv[1] == '1':
    call_command('collectstatic', interactive=False, verbosity=0)
    print('collectstatic done')
