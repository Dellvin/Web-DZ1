from django.core.management.base import BaseCommand

from app.models import Question, LikeComment

from random import randint


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int)


    def handle(self, *args, **options):
        print("Creating users")
        index = 1
        count = options['count']
        while index < count:

            q = Question.objects.get(id=index)
            for c in q.comment_set.all():
                totalLikes = randint(0, 100)
                likes = LikeComment(comment=c, likes=totalLikes)
                likes.save()
                for i in range(totalLikes):
                    likes.users.add(randint(1, 100))

            index += 1

