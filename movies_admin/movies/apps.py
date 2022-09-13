from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MoviesConfig(AppConfig):
    verbose_name = _('movies')
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'
