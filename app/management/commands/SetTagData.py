from django.core.management.base import BaseCommand

from app.models import Tag, Question

from faker import Faker
from random import choices, randint

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--count', type=int)
        parser.add_argument('--count_tags_on_question', type=int)

    def handle(self, *args, **options):
        print("Creating tags")
        fake = Faker()
        uniq = set()
        index = 0
        count = options['count']
        count_tags_on_question = options['count_tags_on_question']
        while index < count:
            profile = fake.profile()

            tagName = profile['username']
            if tagName not in uniq:
                tag = Tag(
                    title=tagName,
                    rating=randint(0, 1000)
                )
                tag.save()
                uniq.add(tagName)
                index += 1
