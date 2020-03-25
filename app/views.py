from django.http import HttpResponse
from django.shortcuts import render

questions = {
    i: {'id': i, 'title': f'Question #{i}'}
    for i in range(5)
}

questionsForTag = {
    i: {'id': i, 'title': f'Question #{i}', 'count': 2}
    for i in range(5)
}

def main(request):
    return render(request, 'main_page.html', {
        'name': 'Ivan',
        'questions': questions.values(),
    })


def singin(request):
    return render(request, 'sing_in_page.html', {})


def singup(request):
    return render(request, 'sing_up_page.html', {})


def newQuestion(request):
    return render(request, 'new_question_page.html', {})


def tagSearch(request, tag):
    return render(request, 'tag_search_page.html', {
        'tag': tag,
        'questionsTag': questionsForTag.values(),
    })

def question(request, qid):
    quest = questions.get(qid)

    answers = {
        i: {'id': i, 'title': f'Answer #{i}'}
        for i in range(5)
    }

    return render(request, 'question_page.html', {
        'question': quest,
        'answers': answers,
    })


def settings(request):
    return render(request, 'settings_page.html', {})

