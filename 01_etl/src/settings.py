import os

from pydantic import BaseSettings


class Settings(BaseSettings):

    postgres_dsl: dict = {
        'dbname': os.environ.get("DB_NAME", 'movies_database'),
        'user': os.environ.get("DB_USER", 'app'),
        'password': os.environ.get("DB_PASSWORD", '123qwe'),
        'host': os.environ.get("DB_HOST", 'localhost'),
        'port': os.environ.get("DB_PORT", '5432')}

    elasticsearch_connect: str = os.environ.get("ELASTICSEARCH", 'http://localhost:9200')
    research_time: float = os.environ.get("RESEARCH_TIME", '0.1')
    postgres_fetchsize: int = os.environ.get('DB_FETCHSIZE', '1000')
