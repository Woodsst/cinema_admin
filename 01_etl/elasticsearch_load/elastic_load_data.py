from elasticsearch import Elasticsearch, helpers

from elasticsearch_load.movie_model import Movie
from src.logging_config import logger


class ElasticLoad:
    def __init__(self, con: Elasticsearch):
        self.con = con

    def load_movies(self, movies_list: list[Movie]):
        """Loading movies in elasticserch"""

        movies_for_bulk = [{
            '_index': x.index,
            '_id': x.fw_id,
            '_type': x.type,
            'actors': x.actors,
            'actors_names': x.actors_names,
            'description': x.description,
            'director': x.director,
            'genre': x.genre,
            'id': x.fw_id,
            'imdb_rating': x.imdb_rating,
            'title': x.title,
            'writers': x.writers,
            'writers_names': x.writers_names
        } for x in movies_list]
        logger.info(f'load in elasticsearch movies - {movies_for_bulk}')
        helpers.bulk(self.con, movies_for_bulk)
