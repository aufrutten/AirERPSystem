#!/bin/sh


echo "Waiting for postgres..."
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
    sleep 0.1
done
echo "PostgresSQL started"

python3 manage.py collectstatic --noinput &
python3 manage.py migrate --noinput || exit 1

if [ -n "$DEBUG" ]; then
  python3 manage.py runserver 0.0.0.0:8080
else
  gunicorn --bind 0.0.0.0:8080 --forwarded-allow-ips="nginx" -w 4 backend.wsgi
fi
