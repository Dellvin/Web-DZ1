# coding=utf-8
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.models import Question, Client, Comment, Tag, LikeQuestion, LikeComment, DisLikeQuestion, DisLikeComment
from django.utils import timezone

questionsNum = {
    i: {'id': i, 'title': f'Question #{i}'}
    for i in range(25)
}

questionsForTag = {
    i: {'id': i, 'title': f'Question #{i}', 'count': 2}
    for i in range(5)
}



def main(request):
    contact_list = list(Question.objects.hot())  # list(questionsNum.objects.hot())
    paginator = Paginator(contact_list, 5)  # По 2 на страницу
    tags=Tag.objects.best_tags()[0:10]
    users=Client.objects.best_members()[0:10]
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


def question(request, qid):
    quest = Question.objects.get(id=qid)
    answers = quest.comment_set.all()
    tags=Tag.objects.best_tags()[0:10]
    users=Client.objects.best_members()[0:10]
    return render(request, 'question_page.html', {
        'question': quest,
        'answers': answers,
        'tags': tags,
        'users': users,
    })


def singin(request):
    tags=Tag.objects.best_tags()[0:10]
    users=Client.objects.best_members()[0:10]
    return render(request, 'sing_in_page.html', {
        'tags': tags,
        'users': users,
    })


def singup(request):
    tags=Tag.objects.best_tags()[0:10]
    users=Client.objects.best_members()[0:10]
    return render(request, 'sing_up_page.html', {
        'tags': tags,
        'users': users,
    })


def newQuestion(request):
    tags=Tag.objects.best_tags()[0:10]
    users=Client.objects.best_members()[0:10]
    return render(request, 'new_question_page.html', {
        'tags': tags,
        'users': users,
    })


def tagSearch(request, tag):
    tags=Tag.objects.best_tags()[0:10]
    users=Client.objects.best_members()[0:10]
    t = Tag.objects.filter(title=tag).first()

    contact_list = list(t.question_set.all())  # list(questionsNum.objects.hot())
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
    tags=Tag.objects.best_tags()[0:10]
    users=Client.objects.best_members()[0:10]
    return render(request, 'settings_page.html', {
        'tags': tags,
        'users': users,
    })


def newest(request):
    tags=Tag.objects.best_tags()[0:10]
    users=Client.objects.best_members()[0:10]
    contact_list = list(Question.objects.newest())  # list(questionsNum.objects.hot())
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