from django.contrib import admin

from .models import Genre, FilmWork, GenreFilmWork, Person, PersonFilmWork
from django.utils.translation import gettext_lazy as _


class PersonFilmWorkInLine(admin.TabularInline):
    model = PersonFilmWork
    autocomplete_fields = ['person']


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonFilmWorkInLine,)
    ordering = ['full_name']
    search_fields = ['full_name']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork
    autocomplete_fields = ['genre']


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmWorkInline, PersonFilmWorkInLine,)

    list_display = ('title', 'type', 'creation_date', 'rating', 'get_genres')

    list_prefetch_related = ['film_work_genres']

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ', '.join([genre.name for genre in obj.film_work_genres.all()])

    get_genres.short_description = _('genres')

    list_filter = ('type',)

    search_fields = ('title', 'description', 'id')
