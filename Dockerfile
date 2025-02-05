FROM alpine:3.18

ADD *.py /bot/
ADD fingerprints.sh /bot/fingerprints.sh
ADD nginx_conf /bot/nginx_conf
ADD requirements.txt  /bot/requirements.txt
ADD /internal/** /bot/internal/**
RUN apk update && apk upgrade
RUN apk add --update py-pip
RUN apk add --update bash 
RUN apk add --update openssl 
RUN pip install -r /bot/requirements.txt 