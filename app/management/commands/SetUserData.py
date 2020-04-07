from django.core.management.base import BaseCommand

from app.models import Client

from faker import Faker

from random import randint

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int)


    def handle(self, *args, **options):
        print("Creating users")
        fake = Faker()
        uniq = set()
        index = 0
        count = options['count']
        while index < count:
            profile = fake.profile()

            username = profile['username']
            if username not in uniq:
                user = Client(
                    login=username,
                    password=profile['username'],
                    email=profile['mail'],
                    rating=randint(0, 100)

                )
                user.save()
                uniq.add(username)
                index += 1
