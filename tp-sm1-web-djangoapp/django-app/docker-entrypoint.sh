#!/bin/sh

server_host="db"
sleep_seconds=5

while true; do
    echo -n "Checking $server_host status... "

    output=$(nc $server_host 3306)

    if [ "$output" != "" ]
    then
        echo "$server_host is running and ready to process requests."
        break
    fi

    echo "$server_host is warming up. Trying again in $sleep_seconds seconds..."
    sleep $sleep_seconds
done


python3 manage.py makemigrations
python3 manage.py migrate
gunicorn -b 0.0.0.0:1488 --env DJANGO_SETTINGS_MODULE=Django_web.settings Django_web.wsgi --access-logfile /var/log/access.log --log-file /var/log/gunicorn.log
