# Generated by Django 3.2 on 2022-09-26 04:42

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunSQL("CREATE SCHEMA IF NOT EXISTS content;"),
        migrations.CreateModel(
            name='FilmWork',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description')),
                ('permission', models.TextField(null=True, verbose_name='permission')),
                ('rating', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='rating')),
                ('creation_date', models.DateField(blank=True, null=True, verbose_name='creation date')),
                ('file_path', models.TextField(blank=True, null=True, max_length=512)),
                ('type', models.CharField(choices=[('mv', 'movie'), ('tv', 'tv show')], max_length=17, verbose_name='type')),
            ],
            options={
                'verbose_name': 'film work',
                'verbose_name_plural': 'films works',
                'db_table': 'content"."film_work',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'genre',
                'verbose_name_plural': 'genres',
                'db_table': 'content"."genre',
            },
        ),
        migrations.CreateModel(
            name='GenreFilmWork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'genre',
                'verbose_name_plural': 'genres',
                'db_table': 'content"."genre_film_work',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=255, verbose_name='full name')),
            ],
            options={
                'verbose_name': 'person',
                'verbose_name_plural': 'persons',
                'db_table': 'content"."person',
            },
        ),
        migrations.CreateModel(
            name='PersonFilmWork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('role', models.CharField(blank=True, choices=[('actor', 'actor'), ('director', 'director'), ('operator', 'operator'), ('producer', 'producer'), ('editor', 'editor'), ('screenwriter', 'screenwriter'), ('writer', 'writer')], max_length=255, verbose_name='role')),
                ('film_work', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork')),
                ('person', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, to='movies.person')),
            ],
            options={
                'verbose_name': 'person',
                'verbose_name_plural': 'persons',
                'db_table': 'content"."person_film_work',
            },
        ),
        migrations.AddIndex(
            model_name='person',
            index=models.Index(fields=['full_name'], name='person_full_na_058eac_idx'),
        ),
        migrations.AddField(
            model_name='genrefilmwork',
            name='film_work',
            field=models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork'),
        ),
        migrations.AddField(
            model_name='genrefilmwork',
            name='genre',
            field=models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, to='movies.genre'),
        ),
        migrations.AddIndex(
            model_name='genre',
            index=models.Index(fields=['name'], name='genre_name_bff4c4_idx'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='film_work_genres',
            field=models.ManyToManyField(through='movies.GenreFilmWork', to='movies.Genre'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='persons',
            field=models.ManyToManyField(through='movies.PersonFilmWork', to='movies.Person'),
        ),
        migrations.AddIndex(
            model_name='personfilmwork',
            index=models.Index(fields=['film_work_id'], name='person_film_work_id_idx'),
        ),
        migrations.AddIndex(
            model_name='personfilmwork',
            index=models.Index(fields=['person_id'], name='person_id_idx'),
        ),
        migrations.AddIndex(
            model_name='genrefilmwork',
            index=models.Index(fields=['film_work_id'], name='genre_film_work_id_idx'),
        ),
        migrations.AddIndex(
            model_name='genrefilmwork',
            index=models.Index(fields=['genre_id'], name='genre_id_idx'),
        ),
    ]
