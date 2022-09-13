import enum


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
