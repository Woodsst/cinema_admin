import os

from pydantic import BaseSettings


class Settings(BaseSettings):

    postgres_dsl: dict = {
        'dbname': os.environ.get("DB_NAME"),
        'user': os.environ.get("DB_USER"),
        'password': os.environ.get("DB_PASSWORD"),
        'host': os.environ.get("DB_HOST"),
        'port': os.environ.get("DB_PORT")}

    elasticsearch_connect: str = os.environ.get("ELASTICSEARCH")
    research_time: float = os.environ.get("RESEARCH_TIME")
    postgres_fetchsize: int = os.environ.get('DB_FETCHSIZE')
