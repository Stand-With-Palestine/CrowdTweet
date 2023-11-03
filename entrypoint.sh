#!/bin/bash
if [[ -z "ENVIRONMENT" ]];then
  python /app/manage.py makemigrations
  python /app/manage.py migrate

gunicorn -c config/gunicorn/config.py
