FROM python:3.10

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY requirements.txt requirements.txt
COPY uwsgi/uwsgi.ini uwsgi.ini

RUN apt-get update && apt-get install -y netcat

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

CMD python manage.py collectstatic

RUN groupadd -r web && useradd -d /opt/app -r -g web web \
    && chown web:web -R /opt/app

USER web

COPY . .

EXPOSE 8000
