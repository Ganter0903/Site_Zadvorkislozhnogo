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
from .models import User

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]

def index(request):
    context_data = {
        "menu": menu,
        "title": 'Задворки сложного - официальный сайт',
        "popular_authors": User.objects.annotate(
            followers_count=Count('followers')
        ).order_by('-followers_count')[:4],
    }
    return render(request, 'index.html', context_data)

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def authors(request):
    context_data = {
        'menu': menu, 
        'title': 'Авторы',
        'authors': User.objects.filter(is_active=True)
    }
    return render(request, 'authors.html', context_data)

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
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Zadvorkislozhnogo:auth'))
    user = request.user
    context = {
        "menu": menu,
        "title": "Профиль",
        "first_name": user.first_name,
        "last_name": user.last_name,
        "surname": user.surname or "",
        "avatar": user.get_avatar_url,
        "balance": user.balance,
    }
    return render(request, 'profile.html', context)

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            return HttpResponseBadRequest('Введите ваш email.')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return HttpResponseBadRequest('Пользователь с таким email не найден.')

        alphabet = string.ascii_letters + string.digits
        password =  ''.join(secrets.choice(alphabet) for _ in range(12))
        user.set_password(password)
        user.save()

        send_mail(
            'Восстановление пароля',
            f'Ваш новый пароль: {password}\n\nЕсли вы не запрашивали восстановление пароля, просто проигнорируйте это письмо.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )

        return HttpResponse('Письмо с инструкциями отправлено на ваш email.')
    return render(request, 'forgot_password.html', {'menu': menu, 'title': 'Восстановление пароля'})

def author_profile(request, pk):
    try:
        author = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponseNotFound('<h1>Автор не найден</h1>')
    if author == request.user:
        return HttpResponseRedirect(reverse('Zadvorkislozhnogo:profile'))
    context_data = {
        "menu": menu,
        "title": "Профиль автора",
        "first_name": author.first_name,
        "last_name": author.last_name,
        "surname": author.surname or "",
        "avatar": author.get_avatar_url,
        "subsribers_count": author.subscribers.count(),
        "articles_count": author.audiobook_set.count() + author.story_set.count() + author.poem_set.count(),
        "account_age": (now() - author.date_joined).days, 
    }
    return render(request, 'author_profile.html', context_data)

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

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if not email or not password or not password_confirm:
            return HttpResponseBadRequest('Заполните все поля.')

        if password != password_confirm:
            return HttpResponseBadRequest('Пароли не совпадают.')

        if User.objects.filter(email=email).exists():
            return HttpResponseBadRequest('Пользователь с таким email уже зарегистрирован.')

        user = User.objects.create(email=email, is_active=False)
        user.set_password(password)
        user.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_link = request.build_absolute_uri(reverse('Zadvorkislozhnogo:verify_email', kwargs={'uidb64': uid, 'token': token}))

        send_mail(
            'Подтвердите регистрацию',
            f'Нажмите на ссылку для активации аккаунта: {activation_link}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )

        return HttpResponse('Письмо с подтверждением отправлено на почту.')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse('Аккаунт не активирован.')
        else:
            return HttpResponseBadRequest('Неверный логин или пароль.')

    return render(request, 'auth.html')


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    print(token)
    print(default_token_generator.check_token(user, token))
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Аккаунт успешно активирован.')
    else:
        return HttpResponseBadRequest('Ссылка активации недействительна.')

def logout_view(request):
    logout(request)
    return redirect('/')