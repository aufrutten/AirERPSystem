#!/bin/sh

ABSOLUT_PATH="$(dirname "$(dirname "$(readlink -f "$0")")")"

cd "$ABSOLUT_PATH" || exit 1
DJANGO_SETTINGS_MODULE=backend.test_settings DEBUG=1 python3 manage.py makemigrations
