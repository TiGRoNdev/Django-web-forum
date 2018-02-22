# start from base
FROM ubuntu:xenial
MAINTAINER Igor Nazarov <igoryan.ms@gmail.com>

# install system-wide deps for python and node
RUN apt-get update && apt-get install -y \
		python3 \
		sqlite3 \
		python3-pip \
		python3-dev \
		libmysqlclient-dev

# copy our application code
ADD django-app /django-app
WORKDIR /django-app

# fetch app specific deps
RUN pip3 install -r requirements.txt
RUN apt-get autoremove -y

# expose port
EXPOSE 1488

# start app
CMD sleep 30s && python3 manage.py makemigrations && python3 manage.py migrate && gunicorn -b 0.0.0.0:1488 --env DJANGO_SETTINGS_MODULE=Django_web.settings Django_web.wsgi --access-logfile /var/log/access.log --log-file /var/log/gunicorn.log
