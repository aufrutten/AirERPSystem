#!/bin/sh

ABSOLUT_PATH="$(dirname "$(dirname "$(readlink -f "$0")")")"

cd "$ABSOLUT_PATH" || exit 1
coverage run ./manage.py test --settings=backend.test_settings
coverage report -m --skip-covered --skip-empty
coverage html
