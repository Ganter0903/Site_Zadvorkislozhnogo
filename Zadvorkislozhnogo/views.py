from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]
def index(request):
    posts = User.objects.all()

    return render(request, 'index.html', {'menu': menu, 'title': 'Задворки сложного - официальный сайт'})


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def Authors(request):
    return render(request, 'authors.html', {'menu': menu, 'title': 'Авторы'})

def poetry(request):
    return render(request, 'poetry.html', {'menu': menu, 'title': 'Стихи'})

def stories(request):
    return render(request, 'stories.html', {'menu': menu, 'title': 'Рассказы'})

def article(request):
    return render(request, 'article.html', {'menu': menu, 'title': 'Рассказ'})

def audiobooks(request):
    return render(request, 'audiobooks.html', {'menu': menu, 'title': 'Аудиокниги'})

def blog(request):
    return render(request, 'blog.html', {'menu': menu, 'title': 'Блог'})

def profile(request):
    return render(request, 'profile.html', {'menu': menu, 'title': 'Профиль'})

def auth(request):
    return render(request, 'auth.html', {'menu': menu, 'title': 'Авторизация'})

def register(request):
    return render(request, 'register.html', {'menu': menu, 'title': 'Регистрация'})

def forgot_password(request):
    return render(request, 'forgot_password.html', {'menu': menu, 'title': 'Восстановление пароля'})

def verify(request):
    return render(request, 'verify.html', {'menu': menu, 'title': 'Верификация'})

def author_profile(request):
    return render(request, 'author_profile.html', {'menu': menu, 'title': 'Профиль автора'})

# views.py
def chart_view(request):
    context = {
        'months': ['Янв', 'Фев', 'Мар', 'Апр', 'Май'],
        'subscribers': [141, 135, 150, 142, 148],

        'categories': ['Баллада', 'Поэма', 'Роман в стихах', 'Сонет', 'Романс', 'Басня', 'Эпос'],
        'articles': ["Затмение", "Матери и дети", "Война и наказание", "Прок", "Метель"],
        'views_today': [300, 200, 150, 70, 90, 120, 80],
        'likes': [80, 50, 60, 30, 40, 20, 10],
        'views_month': [4000, 3200, 280, 1500, 2000, 1200, 800],
        'title': 'Аналитика',
    }
    return render(request, 'chart.html', context)
