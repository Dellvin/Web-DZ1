# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import auth
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.models import Question, Client, Comment, Tag, LikeQuestion, LikeComment, DisLikeQuestion, DisLikeComment
from django.contrib.auth import logout
from app import forms

questionsNum = {
    i: {'id': i, 'title': f'Question #{i}'}
    for i in range(25)
}

questionsForTag = {
    i: {'id': i, 'title': f'Question #{i}', 'count': 2}
    for i in range(5)
}


def main(request):
    contact_list = Question.objects.hot()  # list(questionsNum.objects.hot())
    paginator = Paginator(contact_list, 5)  # По 2 на страницу
    tags = Tag.objects.best_tags()[0:10]
    users = Client.objects.best_members()[0:10]
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        # В случае, GET параметр не число
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    return render(request, 'main_page.html', {
        'questions': questions,
        'tags': tags,
        'users': users,
        'flag': 0,
    })


def singin(request):
    if request.method == 'GET':
        form = forms.LoginForm()
    else:
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                next = request.POST.get('next', '/')
                return HttpResponseRedirect(next)  # TODO нормальный редирект на предыдущую страницу

    tags = Tag.objects.best_tags()[0:10]
    users = Client.objects.best_members()[0:10]
    return render(request, 'sing_in_page.html', {
        'tags': tags,
        'users': users,
        'form': form,
    })


def singup(request):
    if request.method == 'GET':
        form = forms.RegistrationForm
    else:
        form = forms.RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            data = form.cleaned_data
            user = auth.authenticate(username=data['username'], password=data['password1'])
            if user is not None:
                auth.login(request, user)
                next = request.POST.get('next', '/')
                return redirect('/main/')  # TODO нормальный редирект на предыдущую страницу

    tags = Tag.objects.best_tags()[0:10]
    users = Client.objects.best_members()[0:10]
    return render(request, 'sing_up_page.html', {
        'tags': tags,
        'users': users,
        'form': form,
    })


@login_required
def newQuestion(request):
    if request.method == 'GET':
        formQuestion = forms.QuestionForm(request.user.username)
        tags = Tag.objects.best_tags()[0:10]
        users = Client.objects.best_members()[0:10]
        return render(request, 'new_question_page.html', {
            'tags': tags,
            'users': users,
            'form': formQuestion,
        })
    formQuestion = forms.QuestionForm(request.user.client, data=request.POST)
    if formQuestion.is_valid():
        question = formQuestion.save()
        return redirect(
            reverse('question', kwargs={'qid': question.pk}))  # TODO нормальный редирект на страницу нового вопроса
    tags = Tag.objects.best_tags()[0:10]
    users = Client.objects.best_members()[0:10]
    return render(request, 'new_question_page.html', {
        'tags': tags,
        'users': users,
        'form': formQuestion,
    })


def tagSearch(request, tag):
    tags = Tag.objects.best_tags()[0:10]
    users = Client.objects.best_members()[0:10]
    t = Tag.objects.filter(title=tag).first()

    contact_list = t.question_set.all()  # list(questionsNum.objects.hot())
    paginator = Paginator(contact_list, 5)  # По 2 на страницу

    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        # В случае, GET параметр не число
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    return render(request, 'main_page.html', {
        'questions': questions,
        'tag': tag,
        'questionsTag': questionsForTag.values(),
        'tags': tags,
        'users': users,
        'flag': 1
    })


def settings(request):
    tags = Tag.objects.best_tags()[0:10]
    users = Client.objects.best_members()[0:10]
    return render(request, 'settings_page.html', {
        'tags': tags,
        'users': users,
    })


def newest(request):
    tags = Tag.objects.best_tags()[0:10]
    users = Client.objects.best_members()[0:10]
    contact_list = Question.objects.newest()  # list(questionsNum.objects.hot())
    paginator = Paginator(contact_list, 5)  # По 2 на страницу

    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        # В случае, GET параметр не число
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    return render(request, 'main_page.html', {
        'questions': questions,
        'tags': tags,
        'users': users,
        'flag': 1
    })


def logout_view(request):
    logout(request)
    return redirect('/main/')


@login_required
def newQuestion(request):
    if request.method == 'GET':
        formQuestion = forms.QuestionForm(request.user.username)
        tags = Tag.objects.best_tags()[0:10]
        users = Client.objects.best_members()[0:10]
        return render(request, 'new_question_page.html', {
            'tags': tags,
            'users': users,
            'form': formQuestion,
        })
    formQuestion = forms.QuestionForm(request.user.client, data=request.POST)
    if formQuestion.is_valid():
        question = formQuestion.save()
        return redirect(
            reverse('question', kwargs={'qid': question.pk}))
    users = Client.objects.best_members()[0:10]
    tags = Tag.objects.best_tags()[0:10]
    return render(request, 'new_question_page.html', {
        'tags': tags,
        'users': users,
        'form': formQuestion,
    })


def question(request, qid):
    if request.method == 'GET':
        form = forms.AnswerForm(request.user.username)
        quest = Question.objects.get(id=qid)
        answers = quest.comment_set.all()
        tags = Tag.objects.best_tags()[0:10]
        users = Client.objects.best_members()[0:10]
        return render(request, 'question_page.html', {
            'question': quest,
            'answers': answers,
            'tags': tags,
            'users': users,
            'form': form,
        })
    else:
        form = forms.AnswerForm(request.user.client, data=request.POST)
        if form.is_valid():
            form.save(qid)
            redir = '/question/'
            redir += str(qid)
            redir += '/'
            return redirect(redir)
