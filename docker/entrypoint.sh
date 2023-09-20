#!/bin/sh

if [ -z ${LOG_LEVEL} ]; then
export LOG_LEVEL="debug"
fi

if [ -z ${HTTP_PORT} ]; then
export HTTP_PORT=":8000"
fi
if [ -z ${HTTP_WORKERS} ]; then
export HTTP_WORKERS=2
fi
if [ -z ${REDIS_SERVER} ]; then
export REDIS_SERVER="redis"
fi

# wait for redis
echo "Waiting for redis..."
while ! nc -z $REDIS_SERVER 6379; do
  sleep 0.1
done

export FLASK_APP=app.api.main:app

status=$?
if [ $status -eq 0 ]; then
  echo "Starting Gunicorn..."
  gunicorn --workers $HTTP_WORKERS \
           --worker-class=gthread \
           --reload $FLASK_APP \
          -b $HTTP_PORT \
          --timeout 120 \
          --log-level $LOG_LEVEL \
          --log-file=-
else
  echo "Error initializing server, exiting..."
fi
