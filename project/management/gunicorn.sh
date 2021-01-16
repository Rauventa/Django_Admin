#!/bin/bash

NAME="webserver"

PROJECT_DIR=/root/reservation/
VIRTUALENV_DIR=/root/virtualenv/
SOCKET=/root/sock/webserver.sock

USER=root
GROUP=root

env LANG="ru_RU.UTF-8"
env LC_ALL="ru_RU.UTF-8"
env LC_LANG="ru_RU.UTF-8"

WORKERS=2

echo "Starting $NAME with workers $WORKERS"

cd $VIRTUALENV_DIR
source /root/virtualenv/bin/activate
cd $PROJECT_DIR
export PYTHONPATH=$VIRTUALENV_DIR:$PYTHONPATH

exec gunicorn project.wsgi:application --log-file=- --name=$NAME --workers=$WORKERS --user=$USER --group=$GROUP \
--log-level=info --bind=unix:$SOCKET --timeout=500