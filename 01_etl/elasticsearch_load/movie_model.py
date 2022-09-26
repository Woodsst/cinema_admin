from typing import Union

from pydantic import BaseModel


class ModelForElastic(BaseModel):
    index: str = 'movies'
    type: str = '_doc'


class Movie(ModelForElastic):
    actors: list[dict] = []
    actors_names: list = []
    description: Union[str, None] = ''
    director: str = ''
    genre: list[str] = []
    fw_id: str = ''
    imdb_rating: Union[float, None] = 0.0
    title: str = ''
    writers: list[dict] = []
    writers_names: list[str] = []


class Genre(ModelForElastic):
    index: str = 'genres'
    genre: str = ''
    id: str = ''
