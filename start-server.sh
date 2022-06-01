#!/usr/bin/env bash

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (cd coinr; python manage.py createsuperuser --no-input)
fi
(cd coinr; python manage.py migrate --no-input; gunicorn coinr.wsgi --timeout 1000 --worker-tmp-dir /dev/shm --bind 0.0.0.0:$PORT --reload)
