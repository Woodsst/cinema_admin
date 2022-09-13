import datetime
from typing import Generator, Union
from postgres_extractor.tables import Tables
from elasticsearch_load.movie_model import Movie
from src.logging_config import logger


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

            changed_ids = cur.fetchall()
            if len(changed_ids) == 0:
                return
            time_last_update = str(changed_ids[-1]['modified'])
            changed_ids = tuple([x['id'] for x in changed_ids])

            logger.info(f'table - {table}, changes found in {changed_ids}')

            if len(changed_ids) == 1:
                changed_ids = f"('{changed_ids[0]}')"

            if table == Tables.FILMWORK:
                film_work_result = self.extract_data_for_load_in_elastic(changed_ids)
                yield film_work_result, time_last_update

            else:
                modify_filmworks_ids = self.load_modified_id(
                    changed_ids,
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

            changed_filmwork_ids = cur.fetchall()

            if len(changed_filmwork_ids) == 1:
                return f"('{changed_filmwork_ids[0][0]}')"

            return tuple([x['id'] for x in changed_filmwork_ids])

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
                filmworks_data = cur.fetchmany(self.fetch_size)

                if len(filmworks_data) == 0:
                    return
                yield self.formatting(filmworks_data)

    def formatting(self, filmworks_data: list) -> list[Movie]:
        """Formate data for load in elasticsearch"""

        movies = []
        first = filmworks_data[0]
        s = Movie(
            fw_id=first['fw_id'],
            description=first['description'],
            imdb_rating=first['rating'],
            title=first['title'],
        )

        for movie in filmworks_data:

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

            if movie == filmworks_data[-1]:
                movies.append(s)

        return movies
