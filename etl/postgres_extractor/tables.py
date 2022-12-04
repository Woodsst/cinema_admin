import enum
from dataclasses import dataclass


@dataclass
class Table:
    NAME: str
    ID: str
    FOREIGN_KEY: str


@dataclass
class Genre(Table):
    NAME = 'genre'
    ID = 'genre_id'
    FOREIGN_KEY = 'genre_film_work'


@dataclass
class Person(Table):
    NAME = 'person'
    ID = 'person_id'
    FOREIGN_KEY = 'person_film_work'


@dataclass
class Filmwork(Table):
    NAME = 'film_work'


@dataclass
class Tables:
    PERSON = Person
    GENRE = Genre
    FILMWORK = Filmwork

    tables_set: tuple = (PERSON, GENRE, FILMWORK)


class Roles(enum.Enum):
    ACTOR = 'actor'
    DIRECTOR = 'director'
    WRITER = 'writer'
