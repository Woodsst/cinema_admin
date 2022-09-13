from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import FilmWork, PersonFilmWork


class MoviesApiMixin:
    model = FilmWork
    http_method_names = ['get']

    def get_queryset(self):
        films = self.model.objects.annotate(genres=ArrayAgg('film_work_genres__name', distinct=True),
                                            actors=ArrayAgg('persons__full_name',
                                                            filter=Q(personfilmwork__role=PersonFilmWork.Roles.ACTOR),
                                                            distinct=True),
                                            directors=ArrayAgg('persons__full_name',
                                                               filter=Q(
                                                                   personfilmwork__role=PersonFilmWork.Roles.DIRECTOR),
                                                               distinct=True),
                                            writers=ArrayAgg('persons__full_name',
                                                             filter=Q(personfilmwork__role=PersonFilmWork.Roles.WRITER),
                                                             distinct=True)
                                            ).values()
        return films

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, self.paginate_by
        )

        prev, next_page = None, None

        if page.number > 1:
            prev = page.previous_page_number()

        if page.number < paginator.num_pages:
            next_page = page.next_page_number()

        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': prev,
            'next': next_page,
            'results': list(queryset)
        }

        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_queryset(self):
        film = self.model.objects.annotate(genres=ArrayAgg('film_work_genres__name', distinct=True),
                                           actors=ArrayAgg('persons__full_name',
                                                           filter=Q(personfilmwork__role=PersonFilmWork.Roles.ACTOR),
                                                           distinct=True),
                                           directors=ArrayAgg('persons__full_name',
                                                              filter=Q(
                                                                  personfilmwork__role=PersonFilmWork.Roles.DIRECTOR),
                                                              distinct=True),
                                           writers=ArrayAgg('persons__full_name',
                                                            filter=Q(personfilmwork__role=PersonFilmWork.Roles.WRITER),
                                                            distinct=True)
                                           ).filter(pk=self.kwargs.get('pk')).values()
        return film

    def get_context_data(self, **kwargs):
        return list(self.get_queryset())[0]
