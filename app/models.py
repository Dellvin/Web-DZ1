from django.db import models

from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User


class UserManager(models.Manager):
    def best_members(self):
        return self.order_by('-rating')


class TagManager(models.Manager):
    def best_tags(self):
        return self.order_by('-rating')


class CommentManager(models.Manager):
    def hot(self):
        return self.order_by('-rating')


class QuestionManager(models.Manager):
    def hot(self):
        return self.order_by('-rating')

    def newest(self):
        return self.order_by('-dateTime')

    def tagsearch(self):
        return self.tags.all()


class Client(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Avatar')
    rating = models.IntegerField('rating user', default=0)
    objects = UserManager()

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    title = models.CharField('Tag', max_length=128, unique="true")

    rating = models.IntegerField(default=0)
    objects = TagManager()

    def __str__(self):
        return self.title


class Question(models.Model):
    author = models.ForeignKey(Client, on_delete=models.CASCADE)
    title = models.CharField('Title question', max_length=200)
    text = models.TextField('Text question')
    tags = models.ManyToManyField(Tag, verbose_name="list of tags")
    rating = models.IntegerField('Rating question', default=0)
    dateTime = models.DateTimeField('Publication date')
    objects = QuestionManager()

    def __str__(self):
        return self.title


class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # удаляет все комменты в случае удаления вопроса
    author = models.CharField('Author comment', max_length=50)
    text = models.TextField('Add comment')
    rating = models.BigIntegerField(default=0)
    objects = CommentManager()
    isRihtAnswer = models.BooleanField('it is true if author set this answer', default=0)
    user = models.ForeignKey(Client, on_delete=models.CASCADE, default=True)
    def __str__(self):
        return self.text


class LikeQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    users = models.ManyToManyField(Client)
    likes = models.BigIntegerField(default=0)

    def __int__(self):
        return self.likes


class LikeComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    users = models.ManyToManyField(Client)
    likes = models.BigIntegerField(default=0)

    def __int__(self):
        return self.likes


class DisLikeQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    users = models.ManyToManyField(Client)
    dislikes = models.BigIntegerField(default=0)

    def __int__(self):
        return self.dislikes


class DisLikeComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    users = models.ManyToManyField(Client)
    dislikes = models.BigIntegerField(default=0)

    def __int__(self):
        return self.dislikes
