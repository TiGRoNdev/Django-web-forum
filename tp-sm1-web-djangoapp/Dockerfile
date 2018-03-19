# start from base
FROM ubuntu:xenial
MAINTAINER Igor Nazarov <igoryan.ms@gmail.com>

# Local directory with project source
ENV DOCKPROJ_SRC=django-app
# Directory in container for all project files
ENV DOCKPROJ_SRVHOME=/srv
# Directory in container for project source files
ENV DOCKPROJ_SRVPROJ=/srv/backend_server

# install system-wide deps for python and node
RUN apt-get update && apt-get install -y \
		python3 \
		sqlite3 \
		python3-pip \
		python3-dev \
		libmysqlclient-dev \
                netcat

# Create application subdirectories
WORKDIR $DOCKPROJ_SRVHOME
VOLUME ["$DOCKPROJ_SRVPROJ"]

# Copy application source code to SRCDIR
COPY $DOCKPROJ_SRC $DOCKPROJ_SRVPROJ

# fetch app specific deps
RUN pip3 install -r backend_server/requirements.txt
RUN apt-get autoremove -y

WORKDIR $DOCKPROJ_SRVPROJ
RUN chmod 777 docker-entrypoint.sh

EXPOSE 9050

CMD ./docker-entrypoint.sh
