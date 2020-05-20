# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import auth
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.models import Question, Client, Comment, Tag
from django.contrib.auth import logout, update_session_auth_hash
from app import forms
from app.forms import SettingsForm, SettingsAvatarForm

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
            if request.user is not None:
                auth.login(request, request.user)
                return HttpResponseRedirect('/main/')  # TODO нормальный редирект на предыдущую страницу

    tags = Tag.objects.best_tags()[0:10]
    users = Client.objects.best_members()[0:10]
    return render(request, 'sing_in_page.html', {
        'tags': tags,
        'users': users,
        'form': form,
        'errors': form.errors,
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
        'errors': form.errors,
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
        'errors': formQuestion.errors,
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
        'flag': 1,
    })


# def settings(request):
#     tags = Tag.objects.best_tags()[0:10]
#     users = Client.objects.best_members()[0:10]
#     return render(request, 'settings_page.html', {
#         'tags': tags,
#         'users': users,
#         'user': request.user,
#     })

def settings(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=request.user)
        formAv = SettingsAvatarForm(request.user, request.POST, request.FILES)
        if formAv.is_valid():
            formAv.save()
        if form.is_valid():
            form.save()
            return redirect('/main/')
        tags = Tag.objects.best_tags()[0:10]
        users = Client.objects.best_members()[0:10]
        return render(request, 'settings_page.html', {
            'tags': tags,
            'users': users,
            'form': form,
            'formAv': formAv,
            'user': request.user,
            'errors': form.errors,
        })
    else:
        form = SettingsForm(instance=request.user)
        formAv = SettingsAvatarForm(request.user)
        tags = Tag.objects.best_tags()[0:10]
        users = Client.objects.best_members()[0:10]
        return render(request, 'settings_page.html', {
            'tags': tags,
            'users': users,
            'form': form,
            'formAv': formAv,
            'user': request.user,
            'errors': form.errors,
        })


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/settings/')
        else:
            return redirect('/change-password/')
    else:
        form = PasswordChangeForm(user=request.user)
        tags = Tag.objects.best_tags()[0:10]
        users = Client.objects.best_members()[0:10]
        return render(request, 'change_password_page.html', {
            'tags': tags,
            'users': users,
            'form': form,
            'errors': form.errors,
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
        'errors': formQuestion.errors,
    })


def question(request, qid):
    if request.method == 'GET':
        form = forms.AnswerForm(request.user.username)
        quest = Question.objects.get(id=qid)
        answers = quest.comment_set.all()
        tags = Tag.objects.best_tags()[0:10]
        users = Client.objects.best_members()[0:10]
        print()
        return render(request, 'question_page.html', {
            'question': quest,
            'answers': answers,
            'tags': tags,
            'users': users,
            'form': form,
        })
    else:
        if not request.user.is_anonymous:
            url = addComment(request, qid)
            return redirect(url)
        return redirect('/singIn/')  # TODO нормальный редирект на страницу нового вопроса


@login_required
def addComment(request, qid):
    form = forms.AnswerForm(request.user.client, data=request.POST)
    if form.is_valid():
        form.save(qid)
        redir = '/question/'
        redir += str(qid)
        redir += '/'
        return redir


# @login_required_ajax
# def addComment(request, qid):
#     form = forms.AnswerForm(request.user.client, data=request.POST)
#     if form.is_valid():
#         comment=form.save(qid)
#         return HttpResponseAjax(qid=comment.id)
#     else:
#         return HttpResponseAjaxError(
#             code='bad_params',
#             message=form.errors.as_text(),
#         )


def like(request):
    if request.GET:
        url = request.GET['qid']
        return JsonResponse('ok')
    else:
        if request.user.is_anonymous:
            return JsonResponse({
                'errors': 'ANONYMOUS_USER',
            })
        print("AJAX: " + request.POST['id'] + "->" + request.POST['type'])
        if (request.POST['type'] == 'q'):
            q = Question.objects.get(id=request.POST['id'])
            likeModel = q.likequestion_set.get(question=q)
            for client in likeModel.users.all():
                if client.user.username == request.user.username:
                    return JsonResponse({
                        'likes': "",
                        'errors': 'ALREADY_LIKED',
                    })

            dislikeModel = q.dislikequestion_set.get(question=q)

            for client in dislikeModel.users.all():
                if client.user.username == request.user.username:
                    dislikeModel.users.remove(client)

            print(likeModel.users.all())
            q.rating = q.rating + 1
            likeModel.likes = likeModel.likes + 1
            likeModel.users.add(request.user.client)
            q.save()
            likeModel.save()

            return JsonResponse({
                'likes': q.rating,
                'errors': '',
            })
        if request.POST['type'] == 'c':
            answer = Comment.objects.get(id=request.POST['id'])
            likeModel = answer.likecomment_set.get(comment=answer)
            for client in likeModel.users.all():
                if client.user.username == request.user.username:
                    return JsonResponse({
                        'likes': "",
                        'errors': 'ALREADY_LIKED',
                    })
            dislikeModel = answer.dislikecomment_set.get(comment=answer)
            for dis in dislikeModel.users.all():
                if dis.user.username == request.user.username:
                    dislikeModel.users.remove(dis)
            print(likeModel.users.all())
            answer.rating = answer.rating + 1
            likeModel.likes = likeModel.likes + 1
            likeModel.users.add(request.user.client)
            answer.save()
            likeModel.save()
            return JsonResponse({
                'likes': answer.rating,
                'errors': '',
            })


def dislike(request):
    if request.GET:
        url = request.GET['qid']
        return JsonResponse('ok')
    else:
        if request.user.is_anonymous:
            return JsonResponse({
                'errors': 'ANONYMOUS_USER',
            })
        print("AJAX: " + request.POST['id'] + "->" + request.POST['type'])
        if (request.POST['type'] == 'q'):
            q = Question.objects.get(id=request.POST['id'])
            dislikeModel = q.dislikequestion_set.get(question=q)
            for client in dislikeModel.users.all():
                if client.user.username == request.user.username:
                    return JsonResponse({
                        'likes': "",
                        'errors': 'ALREADY_DISLIKED',
                    })
            likeModel = q.likequestion_set.get(question=q)
            for client in likeModel.users.all():
                if client.user.username == request.user.username:
                    likeModel.users.remove(client)

            print(dislikeModel.users.all())
            q.rating = q.rating - 1
            dislikeModel.likes = dislikeModel.dislikes + 1
            dislikeModel.users.add(request.user.client)
            q.save()
            dislikeModel.save()

            return JsonResponse({
                'likes': q.rating,
                'errors': '',
            })
        if request.POST['type'] == 'c':
            q = Comment.objects.get(id=request.POST['id'])
            dislikeModel = q.dislikecomment_set.get(comment=q)
            for client in dislikeModel.users.all():
                if client.user.username == request.user.username:
                    return JsonResponse({
                        'likes': "",
                        'errors': 'ALREADY_DISLIKED',
                    })

            likeModel = q.likecomment_set.get(comment=q)
            for like in likeModel.users.all():
                if like.user.username == request.user.username:
                    likeModel.users.remove(like)
            print(dislikeModel.users.all())
            q.rating = q.rating - 1
            dislikeModel.likes = dislikeModel.dislikes + 1
            dislikeModel.users.add(request.user.client)
            q.save()
            dislikeModel.save()
            return JsonResponse({
                'likes': q.rating,
                'errors': '',
            })


def rightAnswer(request):
    if request.GET:
        return JsonResponse('ok')
    else:
        if request.user.is_anonymous:
            return JsonResponse({
                'errors': 'ANONYMOUS_USER',
            })

        print("AJAX: " + request.POST['id'] + "->" + request.POST['type'])

        answer = Comment.objects.get(id=request.POST['id'])
        make = True
        if answer.isRihtAnswer == True:
            answer.isRihtAnswer = False
        else:
            answer.isRihtAnswer = True
            make = False
        answer.save()
        return JsonResponse({
            'makeit': make,
            'errors': '',
        })
