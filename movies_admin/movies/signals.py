import datetime
from django.db.models.signals import post_save


def attention(sender, instance, created, **kwargs):
    if created and instance.creation_date == datetime.date.today():
        print(f"Сегодня премьера {instance.title}! 🥳")


post_save.connect(receiver=attention, sender='movies.FilmWork',
                  weak=True, dispatch_uid='attention_signal')
