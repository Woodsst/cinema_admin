FROM python:3.10

WORKDIR /opt/app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y netcat

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

RUN groupadd -r web && useradd -d /opt/app -r -g web web \
    && chown web:web -R /opt/app

USER web

COPY . .
