from django.core.management.base import BaseCommand

from app.models import Question, DisLikeQuestion

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
            totalLikes = randint(0, 50)
            likes = DisLikeQuestion(question=q, dislikes=totalLikes)
            likes.save()
            for i in range(totalLikes):
                likes.users.add(randint(1, 100))

            index += 1
