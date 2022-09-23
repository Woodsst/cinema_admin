import datetime
import os
import time

import psycopg2
from elasticsearch import Elasticsearch
from psycopg2.extras import DictCursor

from src.logging_config import logger
from elasticsearch_load.elastic_load_data import ElasticLoad
from postgres_extractor.extract_postgres import PostgresExtractor
from postgres_extractor.tables import Genre, Person, Filmwork, Tables
from src.backoff import backoff
from src.state import State, JsonFileStorage
from src.settings import Settings


class ETL:
    def __init__(self, postgres_con,
                 elasticsearch_con,
                 research_time: float,
                 fetchsize: int):
        self.elastic = ElasticLoad(elasticsearch_con)
        self.postgres = PostgresExtractor(con=postgres_con, fetch_size=fetchsize)
        self.state = self.init_state()
        self.research_time = research_time

    @staticmethod
    def init_state():
        """Install initial state"""

        state_file = JsonFileStorage('./state.json')

        if 'state.json' not in os.listdir(os.getcwd()):
            zero_time = str(datetime.datetime.min)
            state_form = {
                Genre.NAME: zero_time,
                Person.NAME: zero_time,
                Filmwork.NAME: zero_time
            }
            state_file.save_state(state_form)

        return State(state_file)

    def run(self):
        """A loop for checking change in postgres
        tables and update data in elasticsearch"""

        while True:
            time.sleep(self.research_time)

            for table in Tables.tables_set:
                state = self.state.get_state(table.NAME)
                postgres_check = self.postgres.check_update_table(state,
                                                                  table)
                for data, time_update in postgres_check:
                    if data is None:
                        self.state.set_state(table.NAME,
                                             time_update)
                        continue
                    self.elastic.load_movies(data.get('movies'))
                    self.elastic.load_genres(data.get('genres'))
                    self.state.set_state(table.NAME,
                                         time_update)


@backoff()
def main(settings: Settings):
    """Connect postgres and elasticsearch for ETL run"""

    with psycopg2.connect(**settings.postgres_dsl, cursor_factory=DictCursor) as postgres_con, Elasticsearch(
            settings.elasticsearch_connect) as elastic:
        elastic.info()

        etl = ETL(postgres_con=postgres_con,
                  elasticsearch_con=elastic,
                  research_time=settings.research_time,
                  fetchsize=settings.postgres_fetchsize)
        logger.info('app start')
        etl.run()


if __name__ == "__main__":
    settings = Settings()
    main(settings)
