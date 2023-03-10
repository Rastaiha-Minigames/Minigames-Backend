# pull official base image
FROM python:3.10.8

# set work directory
WORKDIR /usr/src/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# soundfile
RUN apt update -y && apt install libsndfile1 gcc -y
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# install dependencies
RUN pip install --upgrade pip setuptools
RUN pip install psycopg2 && pip install --upgrade incremental

# copy requirements
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt


WORKDIR /usr/src/app/

# copy entrypoint-prod.sh
COPY ./entrypoint.prod.sh ./entrypoint.prod.sh

ADD ["./rasta", "./rasta"]
ADD ["./TeamData", "./TeamData"]
ADD ["./frequencyWorkshop", "./frequencyWorkshop"]
ADD ["./imageWorkshop", "./imageWorkshop"]
ADD ["./media", "./media"]
ADD ["./citygame", "./citygame"]

COPY ./manage.py ./manage.py

RUN adduser --disabled-password --gecos '' utillity_api --no-create-home

RUN mkdir -p /usr/src/app/logging && chown -R utillity_api /usr/src/app/logging \
        && mkdir -p /usr/src/app/staticfiles && chown -R utillity_api /usr/src/app/staticfiles \
        && mkdir -p /usr/src/app/media && chown -R utillity_api /usr/src/app/media

RUN chown -R utillity_api /usr/src/app/

# matplotlib
RUN mkdir -m 777 /tmp/NUMBA_CACHE_DIR /tmp/MPLCONFIGDIR
ENV NUMBA_CACHE_DIR=/tmp/NUMBA_CACHE_DIR/
ENV MPLCONFIGDIR=/tmp/MPLCONFIGDIR/

USER utillity_api

# run entrypoint.prod.sh
ENTRYPOINT ["/usr/src/app/entrypoint.prod.sh"]
