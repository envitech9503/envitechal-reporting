sudo pkill gunicorn

sudo gunicorn \
  --bind unix:/run/gunicorn.sock \
  --workers=2 \
  --timeout 200 \
  EnviTechAlApp.wsgi:application \
  --daemon \
  --error-logfile error.log \
  --access-logfile access.log \
  --capture-output \
  --log-level debug


# sudo pkill gunicorn
# sudo gunicorn  --bind unix:/run/gunicorn.sock  --workers=2 --timeout 10200 EnviTechAlApp.wsgi:application  --daemon --reload --error-logfile error.log --access-logfile access.log --capture-output --log-level debug


#!/bin/bash

# Stop existing Gunicorn processes
#sudo pkill gunicorn

# Activate virtualenv
#source /home/django/EnviTechAlApp/venv/bin/activate

# Start Gunicorn in background
#gunicorn EnviTechAlApp.wsgi:application \
#  --bind 127.0.0.1:8000 \
#  --workers 2 \
#  --timeout 7200 \
#  --daemon \
#  --reload \
#  --error-logfile error.log \
#  --access-logfile access.log \
#  --capture-output \
#  --log-level debug
