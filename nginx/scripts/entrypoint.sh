#!/bin/sh
if [ -n "$DEBUG" ]; then
  sleep 5
  /docker-entrypoint.sh nginx -g "daemon off;"
else
  /docker-entrypoint.sh nginx -g "daemon off;"
fi
