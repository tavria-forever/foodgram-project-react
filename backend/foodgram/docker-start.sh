#! /usr/bin/env bash

python3 manage.py migrate
python3 manage.py loaddata fixtures.json
python3 manage.py collectstatic --no-input
gunicorn foodgram.wsgi:application --bind 0:8000
