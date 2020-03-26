#!/bin/bash
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate --run-syncdb
python manage.py shell < init.py