import string
import secrets

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Count
from django.utils.timezone import now
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from Zadvorkislozhnogo.models import User, Poem

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