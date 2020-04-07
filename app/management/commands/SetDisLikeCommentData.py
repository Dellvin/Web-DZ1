from django.core.management.base import BaseCommand

from app.models import Question, DisLikeComment

from random import randint


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int)

    def handle(self, *args, **options):

        index = 1
        count = options['count']
        while index < count:
            q = Question.objects.get(id=index)
            for c in q.comment_set.all():
                totalLikes = randint(0, 100)
                likes = DisLikeComment(comment=c, dislikes=totalLikes)
                likes.save()
                for i in range(totalLikes):
                    likes.users.add(randint(1, 100))

            index += 1


