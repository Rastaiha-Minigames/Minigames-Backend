# pull official base image
FROM python:3.7.4-alpine

# set work directory
WORKDIR /usr/src/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache --virtual .build-deps gcc musl-dev

# install python-dev
RUN apk update \
    && apk add --virtual .build-deps gcc libc-dev libxslt-dev \
    && apk add libffi-dev openssl-dev linux-headers \
    && apk add --no-cache libxslt \
    && pip install lxml==4.5.0

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && pip install --upgrade incremental

# install zlib for pillow
RUN apk add --no-cache jpeg-dev zlib-dev build-base

# install dependencies
RUN pip install --upgrade pip setuptools

# copy requirements
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

# TODO: move it to requirements
RUN pip install django-cors-headers==3.4.0

WORKDIR /usr/src/app/

# copy entrypoint-prod.sh
COPY ./entrypoint.prod.sh ./entrypoint.prod.sh

ADD ["./rasta", "./rasta"]
ADD ["./TeamData", "./TeamData"]
COPY ./manage.py ./manage.py

RUN adduser -D utillity_api

RUN mkdir -p /usr/src/app/logging && chown -R utillity_api /usr/src/app/logging \
        && mkdir -p /usr/src/app/staticfiles && chown -R utillity_api /usr/src/app/staticfiles \
        && mkdir -p /usr/src/app/media && chown -R utillity_api /usr/src/app/media

RUN chown -R utillity_api /usr/src/app/

USER utillity_api

# run entrypoint.prod.sh
ENTRYPOINT ["/usr/src/app/entrypoint.prod.sh"]