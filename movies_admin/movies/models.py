from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from movies.base import TimeStampedMixin, UUIDMixin
import movies.signals


class Genre(TimeStampedMixin, UUIDMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
        indexes = [
            models.Index(fields=('name',))
        ]


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full name'), max_length=255)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('person')
        verbose_name_plural = _('persons')
        indexes = [
            models.Index(fields=('full_name',))
        ]


class FilmWork(TimeStampedMixin, UUIDMixin):
    title = models.CharField(_('title'), max_length=255, blank=True)
    description = models.TextField(_('description'), null=True)
    rating = models.FloatField(
        _('rating'),
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    creation_date = models.DateField(_('creation date'), blank=True, null=True)
    file_path = models.CharField(_('file path'), max_length=512, blank=True, null=True)

    class FilmType(models.TextChoices):
        MOVIE = 'mv', _('movie')
        TV_SHOW = 'tv', _('tv show')

    type = models.CharField(
        _('type'),
        max_length=17,
        choices=FilmType.choices
    )

    class PermissionsType(models.TextChoices):
        USER = 'us', _('user')
        SUBSCRIBER = 'su', _('subscriber')
        ALL = 'al', _('all')

    permission = models.CharField(
        _('permission'),
        max_length=36,
        choices=PermissionsType.choices
    )

    def __str__(self):
        return self.title

    film_work_genres = models.ManyToManyField(Genre, through='GenreFilmWork')
    persons = models.ManyToManyField(Person, through='PersonFilmWork')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('film work')
        verbose_name_plural = _('films works')


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey(FilmWork,
                                  on_delete=models.CASCADE,
                                  db_index=False)
    genre = models.ForeignKey(Genre,
                              on_delete=models.CASCADE,
                              db_index=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.genre.name

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
        indexes = [
            models.Index(fields=['film_work_id'], name='genre_film_work_id_idx'),
            models.Index(fields=['genre_id'], name='genre_id_idx')
        ]


class PersonFilmWork(UUIDMixin):
    film_work = models.ForeignKey(FilmWork,
                                  on_delete=models.CASCADE,
                                  db_index=False)
    person = models.ForeignKey(Person,
                               on_delete=models.CASCADE,
                               db_index=False)

    created = models.DateTimeField(auto_now_add=True)

    class Roles(models.TextChoices):
        ACTOR = 'actor', _('actor')
        DIRECTOR = 'director', _('director')
        OPERATOR = 'operator', _('operator')
        PRODUCER = 'producer', _('producer')
        EDITOR = 'editor', _('editor')
        SCREENWRITER = 'screenwriter', _('screenwriter')
        WRITER = 'writer', _('writer')

    role = models.CharField(_('role'), max_length=255, blank=True,
                            choices=Roles.choices)

    def __str__(self):
        return self.person.full_name

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('person')
        verbose_name_plural = _('persons')
        indexes = [
            models.Index(fields=['film_work_id'], name='person_film_work_id_idx'),
            models.Index(fields=['person_id'], name='person_id_idx')
        ]
