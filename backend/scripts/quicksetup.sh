#!/usr/bin/env bash
python3 manage.py migrate --run-syncdb
DJANGO_SUPERUSER_EMAIL=superuser@gmail.com.invalid DJANGO_SUPERUSER_PASSWORD=qwerty123 python3 manage.py createsuperuser --noinput
python3 manage.py generate_data