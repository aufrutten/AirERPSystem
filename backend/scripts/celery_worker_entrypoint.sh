#!/bin/sh


echo "Waiting for postgres..."
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
    sleep 0.1
done
echo "PostgresSQL started"

sleep 10

if [ -n "$DEBUG" ]; then
  #  Launch with beat if DEBUG mode
  celery -A backend worker --loglevel=info -B
else
  celery -A backend worker --loglevel=info
fi
