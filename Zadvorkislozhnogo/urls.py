from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('Авторы/', Authors, name='authors'),
    path('Стихи/', poetry, name='poetry'),
    path('Рассказы/', stories, name='stories'),
    path('Аудиокниги/', audiobooks, name='audiobooks'),
    path('Блог/', blog, name='blog'),
]