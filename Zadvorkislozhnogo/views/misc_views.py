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

def index(request):
    context_data = {
        "title": 'Задворки сложного - официальный сайт',
        "popular_authors": User.objects.annotate(
            followers_count=Count('followers')
        ).order_by('-followers_count')[:4],
    }
    return render(request, 'index.html', context_data)

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')