#!/bin/bash

echo "building project..."
python3.9 -m pip install -r requirements.txt




python3.9 manage.py collectstatic --noinput --clear
echo "make migration"
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput