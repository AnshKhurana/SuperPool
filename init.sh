#!/bin/bash
dropdb -p 9001 -U superpool pool
createdb -p 9001 -U superpool pool
psql -h localhost -p 9001  -U superpool -d pool   -c  "CREATE EXTENSION pg_trgm;"

python manage.py makemigrations
python manage.py migrate 
python manage.py migrate --run-syncdb
python manage.py shell < init.py