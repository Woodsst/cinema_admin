import datetime
import enum
from typing import Generator, Union

from elasticsearch_load.movie_model import Movie
from src.logging_config import logger


class Genre(enum.Enum):
    NAME = 'genre'
    ID = 'genre_id'
    FOREIGN_KEY = 'genre_film_work'


class Person(enum.Enum):
    NAME = 'person'
    ID = 'person_id'
    FOREIGN_KEY = 'person_film_work'


class Filmwork(enum.Enum):
    NAME = 'film_work'


class Tables(enum.Enum):
    PERSON = Person
    GENRE = Genre
    FILMWORK = Filmwork


class PostgresExtractor:

    def __init__(self, fetch_size: int, con):
        self.con = con
        self.cur = self.con.cursor()
        self.fetch_size = fetch_size

    def check_update_table(self, update_time: datetime, table: Tables) -> Union[Generator, tuple]:
        """Generator for loading changes in the table"""

        with self.con.cursor() as cur:
            cur.execute("""
            SELECT id, modified
            FROM content.{0}
            WHERE modified > '{1}'
            ORDER BY modified
            """.format(table.value.NAME.value, update_time))

            result = cur.fetchall()
            if len(result) == 0:
                return
            time_last_update = str(result[-1]['modified'])
            result = tuple([x['id'] for x in result])

            logger.info(f'table - {table}, changes found in {result}')

            if len(result) == 1:
                result = f"('{result[0]}')"

            if table == Tables.FILMWORK:
                film_work_result = self.extract_data_for_load_in_elastic(result)
                yield film_work_result, time_last_update

            else:
                modify_filmworks_ids = self.load_modified_id(
                    result,
                    id=table.value.ID.value,
                    table=table.value.FOREIGN_KEY.value
                )

                if len(modify_filmworks_ids) == 0:
                    yield None, time_last_update
                    return

                movies = self.extract_data_for_load_in_elastic(modify_filmworks_ids)
                yield movies, time_last_update

    def load_modified_id(self, list_id, id: str, table: str) -> Union[str, tuple]:
        """Load filmworks ids that have been changed"""

        with self.con.cursor() as cur:
            cur.execute("""
            SELECT fw.id
            FROM content.film_work fw
            LEFT JOIN content.{0} pfw ON pfw.film_work_id = fw.id
            WHERE pfw.{1} IN {2}
            ORDER BY fw.modified
            """.format(table, id, list_id))

            result = cur.fetchall()

            if len(result) == 1:
                return f"('{result[0][0]}')"

            return tuple([x['id'] for x in result])

    def extract_data_for_load_in_elastic(self, list_id: tuple) -> Union[list[Movie], None]:
        """Load all movies data for recording in elasticsearch"""

        with self.con.cursor() as cur:
            cur.execute("""
                SELECT
                fw.id as fw_id,
                fw.title,
                fw.description,
                fw.rating,
                fw.type,
                fw.created,
                fw.modified,
                pfw.role,
                p.id,
                p.full_name,
                g.name
            FROM content.film_work fw
            LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
            LEFT JOIN content.person p ON p.id = pfw.person_id
            LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
            LEFT JOIN content.genre g ON g.id = gfw.genre_id
            WHERE fw.id IN {0}
            ORDER BY fw.id;
                """.format(list_id))

            while True:
                result = cur.fetchmany(self.fetch_size)

                if len(result) == 0:
                    return
                yield self.formatting(result)

    def formatting(self, count: list) -> list[Movie]:
        """Formate data for load in elasticsearch"""

        movies = []
        start = count[0]
        s = Movie(
            fw_id=start['fw_id'],
            description=start['description'],
            imdb_rating=start['rating'],
            title=start['title'],
        )

        for movie in count:

            if s.fw_id != movie['fw_id']:
                movies.append(s)
                s = Movie(
                    fw_id=movie['fw_id'],
                    description=movie['description'],
                    imdb_rating=movie['rating'],
                    title=movie['title']
                )

            role = movie['role']
            person_name = movie['full_name']
            person_id = movie['id']
            person = {'id': person_id, 'name': person_name}
            genre = movie['name']

            if role == 'actor' and person not in s.actors:
                s.actors.append({'id': person_id, 'name': person_name})
                s.actors_names.append(person_name)

            if role == 'director' and person_name not in s.director:
                s.director = person_name

            if role == 'writer' and person not in s.writers:
                s.writers.append({'id': person_id, 'name': person_name})
                s.writers_names.append(person_name)

            if genre not in s.genre:
                s.genre.append(genre)

            if movie == count[-1]:
                movies.append(s)

        return movies
