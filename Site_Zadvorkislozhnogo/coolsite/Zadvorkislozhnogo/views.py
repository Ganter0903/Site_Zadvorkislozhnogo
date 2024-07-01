from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]
def index(request):
    posts = Users.objects.all()

    return render(request, 'Zadvorkislozhnogo/index.html', {'menu': menu, 'title': 'Задворки сложного - официальный сайт'})


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def Authors(request):
    return render(request, 'Zadvorkislozhnogo/Authors.html', {'menu': menu, 'title': 'Авторы'})

def poetry(request):
    return render(request, 'Zadvorkislozhnogo/poetry.html', {'menu': menu, 'title': 'Стихи'})

def stories(request):
    return render(request, 'Zadvorkislozhnogo/stories.html', {'menu': menu, 'title': 'Рассказы'})

def audiobooks(request):
    return render(request, 'Zadvorkislozhnogo/audiobooks.html', {'menu': menu, 'title': 'Аудиокниги'})

def blog(request):
    return render(request, 'Zadvorkislozhnogo/blog.html', {'menu': menu, 'title': 'Блог'})
