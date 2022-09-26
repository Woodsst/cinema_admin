from elasticsearch import Elasticsearch, helpers

from elasticsearch_load.movie_model import Movie, Genre
from src.logging_config import logger


class ElasticLoad:
    def __init__(self, con: Elasticsearch):
        self.con = con

    def load_movies(self, movies_list: list[Movie]):
        """Loading movies in elasticserch"""

        movies_for_bulk = [{
            '_index': movie.index,
            '_id': movie.fw_id,
            '_type': movie.type,
            'actors': movie.actors,
            'actors_names': movie.actors_names,
            'description': movie.description,
            'director': movie.director,
            'genre': movie.genre,
            'id': movie.fw_id,
            'imdb_rating': movie.imdb_rating,
            'title': movie.title,
            'writers': movie.writers,
            'writers_names': movie.writers_names
        } for movie in movies_list]
        logger.info(f'load in elasticsearch movies - {movies_for_bulk}')
        helpers.bulk(self.con, movies_for_bulk)

    def load_genres(self, genres_list: list[Genre]):
        """Load genres in elasticsearch"""

        genres_for_bulk = [{
            '_index': genre.index,
            '_id': genre.id,
            '_type': genre.type,
            'genre': genre.genre,
            'id': genre.id}
            for genre in genres_list]

        logger.info(f'load in elasticsearch movies - {genres_for_bulk}')
        helpers.bulk(self.con, genres_for_bulk)
