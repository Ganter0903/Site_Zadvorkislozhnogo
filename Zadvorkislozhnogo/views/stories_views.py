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

def stories(request):
    return render(request, 'stories.html', {'title': 'Рассказы'})

def article(request):
    return render(request, 'article.html', {'title': 'Рассказ'})