FROM ubuntu:16.04

MAINTAINER Igor Nazarov <igoryan.ms@gmail.com>

RUN apt-get update \
	&& debconf-set-selections <<< 'mysql-server mysql-server/root_password password fobloi56' \
	&& debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password fobloi56' \
	&& apt-get -y install mysql-server

ADD my.cnf /etc/mysql/
