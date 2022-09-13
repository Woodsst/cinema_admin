#!/bin/bash
while ! nc -z -v $DB_HOST $DB_PORT; do
      sleep 1
    done

python3 manage.py migrate
uwsgi --ini uwsgi.ini
