mkdir server
cd server
initdb -D pool -U superpool #/usr/lib/postgresql/10/bin/initdb -D pool -U superpool
pg_ctl -D pool -l logfile start #/usr/lib/postgresql/10/bin/pg_ctl -D pool -l logfile start
# edit port number to 9001
# use  psql -h localhost -p 9001  -U superpool -d postgres
# CREATE DATABASE pool;