sudo pkill gunicorn


sudo pkill gunicorn
sudo gunicorn  --bind unix:/run/gunicorn.sock --workers=2 --timeout 7200 EnviTechAlApp.wsgi:application --reload --access-logfile - --error-logfile - --capture-output --log-level debug


#!/bin/bash

#!/bin/bash

#sudo pkill gunicorn

# Activate virtualenv
#source /home/django/EnviTechAlApp/venv/bin/activate

# Start Gunicorn in foreground
#sudo gunicorn EnviTechAlApp.wsgi:application \
#  --bind 127.0.0.1:8000 \
#  --workers 2 \
#  --timeout 7200 \
#  --reload \
# --access-logfile - \
#  --error-logfile - \
#  --log-level debug \
#  --capture-output
