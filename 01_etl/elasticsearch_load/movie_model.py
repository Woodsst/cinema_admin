from typing import Union

from pydantic import BaseModel


class Movie(BaseModel):
    index: str = 'movies'
    type: str = '_doc'
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
