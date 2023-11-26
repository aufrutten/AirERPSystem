#!/bin/sh


echo "Waiting for postgres..."
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
    sleep 0.1
done
echo "PostgresSQL started"

sleep 10

celery -A backend beat --loglevel=info
