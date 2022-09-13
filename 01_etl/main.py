import datetime
import os
import time

import elasticsearch
import psycopg2
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from psycopg2.extras import DictCursor

from elasticsearch_load.elastic_load_data import ElasticLoad
from postgres_extractor.extract_postgres import PostgresExtractor, Tables
from src.logging_config import logger
from src.state import State, JsonFileStorage


class ETL:
    def __init__(self, postgres_con, elasticsearch_con, research_time: int):
        self.elastic = ElasticLoad(elasticsearch_con)
        self.postgres = PostgresExtractor(con=postgres_con, fetch_size=1000)
        self.state = self.init_state()
        self.research_time = research_time

    @staticmethod
    def init_state():
        """Install initial state"""

        state_file = JsonFileStorage('./state.json')

        if 'state.json' not in os.listdir(os.getcwd()):
            zero_time = str(datetime.datetime(1, 1, 1, 0, 0, 0, 0,
                                              tzinfo=datetime.timezone.utc))
            state_form = {
                Tables.GENRE.value.NAME.value: zero_time,
                Tables.PERSON.value.NAME.value: zero_time,
                Tables.FILMWORK.value.NAME.value: zero_time
            }
            state_file.save_state(state_form)

        return State(state_file)

    def run(self):
        """A loop for checking change in postgres
        tables and update data in elasticsearch"""

        while True:
            time.sleep(self.research_time)

            for table in Tables:
                state = self.state.get_state(table.value.NAME.value)
                postgres_check = self.postgres.check_update_table(state,
                                                                  table)
                for data, time_update in postgres_check:
                    if data is None:
                        self.state.set_state(table.value.NAME.value,
                                             time_update)
                        continue
                    for movies in data:
                        self.elastic.load_movies(movies)
                        self.state.set_state(table.value.NAME.value,
                                             time_update)


if __name__ == "__main__":
    load_dotenv()
    postgres_dsl = {'dbname': os.environ.get("DB_NAME"),
                    'user': os.environ.get("DB_USER"),
                    'password': os.environ.get("DB_PASSWORD"),
                    'host': os.environ.get("DB_HOST"),
                    'port': os.environ.get("DB_PORT")}
    connect_postgres_timer = 0
    connect_elastic_timer = 0
    logger.info('app start')

    while True:
        time.sleep(connect_postgres_timer)
        time.sleep(connect_elastic_timer)
        try:

            with psycopg2.connect(**postgres_dsl, cursor_factory=DictCursor) as postgres_con, Elasticsearch(
                    os.environ.get("ELASTICSEARCH")) as elastic:
                elastic.info()
                etl = ETL(postgres_con=postgres_con,
                          elasticsearch_con=elastic,
                          research_time=int(os.environ.get("RESEARCH_TIME")))
                etl.run()

        except psycopg2.InterfaceError:
            logger.warning(f'Database connection break, the next connection request after {connect_postgres_timer} sec')
            connect_postgres_timer += 1
            if connect_postgres_timer == 31:
                connect_postgres_timer = 1

        except psycopg2.OperationalError:
            logger.warning(
                f'Database connection refused, the next connection request after {connect_postgres_timer} sec')
            connect_postgres_timer += 1
            if connect_postgres_timer == 31:
                connect_postgres_timer = 1

        except elasticsearch.exceptions.ConnectionError:
            logger.warning(
                f'Elasticsearch connection refused, the next connection request after {connect_elastic_timer} sec')
            connect_elastic_timer += 1
            if connect_elastic_timer == 31:
                connect_elastic_timer = 1
