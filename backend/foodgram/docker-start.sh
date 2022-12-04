#! /usr/bin/env bash

python3 manage.py migrate
#python3 manage.py loaddata fixtures.json
python manage.py initadmin
#python3 manage.py collectstatic --no-input
gunicorn api_yamdb.wsgi:application --bind 0:8000
