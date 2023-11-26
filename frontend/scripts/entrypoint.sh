#!/bin/sh

if [ -n "$DEBUG" ]; then
  npm install --silent
  npm run dev
else
  npm run build || exit 1
  tail -f "/dev/null"
fi