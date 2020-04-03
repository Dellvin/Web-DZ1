# coding=utf-8
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

questionsNum = {
    i: {'id': i, 'title': f'Question #{i}'}
    for i in range(25)
}

QUESTIONS = {
    '1': {'id': 1, 'title': 'I`m your dream', 'text': 'I`m your dream, make you real'},
    '2': {'id': 2, 'title': 'I`m your eyes', 'text': 'I`m your eyes when you must steal'},
    '3': {'id': 3, 'title': 'I`m your pain', 'text': 'I`m your pain when you can`t feel'},
}

questionsForTag = {
    i: {'id': i, 'title': f'Question #{i}', 'count': 2}
    for i in range(5)
}

def main(request):
    contact_list = list(questionsNum.values())
    paginator = Paginator(contact_list, 5)  # По 2 на страницу

    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        # В случае, GET параметр не число
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    return render(request, 'main_page.html', {'questions': questions})



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
    quest = questionsNum.get(qid)

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

