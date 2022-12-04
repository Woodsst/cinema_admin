# Django панель администратора онлайн кинотеатра c ETL.

## Панель администрирования базы данных фильмов онлайн кинотеатра с ETL для переноса данных из PostgreSQL в Elasticsearch.

## Структура репозитория
* etl - Процесс транспортировки данных из PostgreSQL в Elasticsearch 
* movies_admin - Django админка для работы с фильмами в PostgreSQL
* config - Конфигурация для Nginx

## Запуск сервиса

### Запуск всего сервиса производится через докер
```commandline
$ docker-compose up --build
```
Панель администратора будет доступна по адресу
http://localhost/admin/

### Для создания пользователя
```commandline
docker exec -it <django_container_name> python3 manage.py createsuperuser
```
