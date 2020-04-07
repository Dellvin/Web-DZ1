from django.core.management.base import BaseCommand

from app.models import Client, Question, Comment

from random import choice, randint

from faker import Faker

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--count', type=int)



    def handle(self, *args, **options):
        print("Creating questions")
        fake = Faker()
        index = 1
        count = options['count']
        while index < count:
            max=randint(0, 10)
            for i in range(max):
                profile = fake.profile()
                q=Question.objects.get(id=index)
                comment=q.comment_set.create(
                    author=profile['username'],
                    text=fake.text(max_nb_chars=200, ext_word_list=None),
                    rating=randint(0, 100),
                )
                comment.save()

            index += 1



