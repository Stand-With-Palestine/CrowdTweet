#!/bin/bash
if [[ -z "ENVIRONMENT" ]];then
do
  python /app/manage.py makemigrations
  python /app/manage.py migrate
fi
gunicorn -c config/gunicorn/config.py
