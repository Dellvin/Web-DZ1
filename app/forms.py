from django import forms
from app.models import Question, Tag, Client, Comment, LikeComment, LikeQuestion, DisLikeComment, DisLikeQuestion
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=32, min_length=4)
    password = forms.CharField(widget=forms.PasswordInput, min_length=4, max_length=32)

    def clean_username(self):
        username = self.cleaned_data['username']
        if ' ' in username:
            raise forms.ValidationError('username contains spaces(')
        return username


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, author, *args, **kwargs):
        self.auhtor = author
        super().__init__(*args, **kwargs)

    def save(self, qid, commit=True):
        answer = Comment(text=self.cleaned_data['text'])
        answer.author = self.auhtor
        answer.question = Question.objects.get(id=qid)
        answer.dateTime = timezone.now()

        if commit:
            answer.save()

        like = LikeComment(comment=answer)
        dis = DisLikeComment(comment=answer)
        like.save()
        dis.save()
        return answer


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    def __init__(self, author, *args, **kwargs):
        self.auhtor = author
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        question = Question(title=self.cleaned_data['title'], text=self.cleaned_data['text'])
        question.author = self.auhtor
        question.dateTime = timezone.now()
        if commit:
            question.save()

        dis = DisLikeQuestion(question=question, dislikes=0)
        like = LikeQuestion(question=question, likes=0)
        dis.save()
        like.save()
        question.tags.set(self.cleaned_data['tags'])
        return question


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User

        fields = ("username", "email", 'password1', 'password2')

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            password=self.cleaned_data['password1'],
            email=self.cleaned_data['email'],
        )
        client = Client(user=user)
        user.save()
        client.save()
        return client


class SettingsForm(UserChangeForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']
        exclude = ['password1', 'password2', 'password']


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['avatar']

    def __init__(self, user, *args, **kwargs):
        self.author = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        client = self.author.client
        pic = self.cleaned_data['avatar']
        client.avatar = pic
        client.save()


class AjaxForm(forms.Form):
    idQuestion = forms.IntegerField

    def clean_username(self):
        ID = self.cleaned_data['idQuestion']
        if not ID.is_integer():
            raise forms.ValidationError('id is not integer')
        return ID
