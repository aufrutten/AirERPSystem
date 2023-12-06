#!/bin/sh

ABSOLUT_PATH="$(dirname "$(dirname "$(readlink -f "$0")")")"

cd "$ABSOLUT_PATH" || exit 1
python3 -m venv venv
pip3 install -r requirements.txt
