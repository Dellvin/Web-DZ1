from django.core.management.base import BaseCommand

from app.models import Question, LikeQuestion

from random import randint


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int)

    def get_10_procent(self, number):
        return number // 10

    def handle(self, *args, **options):
        index = 1
        count = options['count']
        while index < count:

            q = Question.objects.get(id=index)
            totalLikes = randint(0, 100)
            likes = LikeQuestion(question=q, likes=totalLikes)
            likes.save()
            for i in range(totalLikes):
                likes.users.add(randint(1, 100))

            index += 1

