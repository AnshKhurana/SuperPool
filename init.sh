#!/bin/bash
dropdb -p 9001 -U superpool pool
createdb -p 9001 -U superpool pool

python manage.py makemigrations
python manage.py migrate 
python manage.py migrate --run-syncdb
python manage.py shell < init.py