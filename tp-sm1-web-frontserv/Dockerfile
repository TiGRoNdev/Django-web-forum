FROM ubuntu:xenial

MAINTAINER Igor Nazarov <igoryan.ms@gmail.com>

RUN apt-get update \
    && apt-get install -y apt-utils \
    && apt-get install -y software-properties-common \
    && apt-add-repository -y ppa:nginx/stable \
    && apt-get update \
    && apt-get install -y nginx \
    && rm -rf /var/lib/apt/lists/*

ADD nginx.conf /etc/nginx/nginx.conf
ADD default.conf /etc/nginx/conf.d/default.conf

ADD static /resources/static

RUN rm /etc/nginx/sites-enabled/default

RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

RUN useradd nginx
RUN usermod -aG nginx nginx

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
