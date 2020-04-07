from django.core.management.base import BaseCommand

from app.models import Client, Question
from random import choice, randint

from faker import Faker


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--count', type=int)

    def handle(self, *args, **options):
        fake = Faker()
        index = 0
        count = options['count']
        while index < count:
            u = Client.objects.get(id=randint(1, 100))
            question = u.question_set.create(
                title=fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None),
                text=fake.text(max_nb_chars=200, ext_word_list=None),
                rating=randint(0, 100),
                dateTime=fake.date_time_between(),
            )
            question.save()
            question.tags.add(randint(1, 100))
            index += 1

# q=Question.objects.get(id=index)
#                 comment=q.comment_set.create(
#                     author=profile['username'],
#                     text=fake.text(max_nb_chars=200, ext_word_list=None),
#                     rating=randint(0, 100),
#                 )
#                 comment.save()
