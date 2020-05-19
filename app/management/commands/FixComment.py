from django.core.management.base import BaseCommand

from app.models import Comment, Client

from django.contrib.auth.models import User

from random import randint


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int)

    def handle(self, *args, **options):
        print("Fixing users")
        index = 1

        for c in Comment.objects.all():
            for cl in Client.objects.all():
                if cl.user.username == c.author:
                    c.user = cl
                    c.save()
                    break

        index += 1
