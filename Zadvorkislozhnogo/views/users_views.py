import string
import secrets

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.timezone import now
from Zadvorkislozhnogo.models import User

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

    return render(request, 'users/register.html')

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

    return render(request, 'users/auth.html')

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

def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Zadvorkislozhnogo:auth'))
    user = request.user
    context = {
        "title": "Профиль",
        "first_name": user.first_name,
        "last_name": user.last_name,
        "surname": user.surname or "",
        "avatar": user.get_avatar_url,
        "balance": user.balance,
    }
    return render(request, 'users/profile.html', context)

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
    return render(request, 'users/forgot_password.html', {'title': 'Восстановление пароля'})

def author_profile(request, pk):
    try:
        author = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponseNotFound('<h1>Автор не найден</h1>')
    if author == request.user:
        return HttpResponseRedirect(reverse('Zadvorkislozhnogo:profile'))
    context_data = {
        "title": "Профиль автора",
        "first_name": author.first_name,
        "last_name": author.last_name,
        "surname": author.surname or "",
        "avatar": author.get_avatar_url,
        "subsribers_count": author.subscribers.count(),
        "articles_count": author.audiobook_set.count() + author.story_set.count() + author.poem_set.count(),
        "account_age": (now() - author.date_joined).days,
        "author_poems": author.poem_set.all().order_by('-created_at'),
        "author_stories": author.story_set.all().order_by('-created_at'),
    }
    return render(request, 'users/author_profile.html', context_data)

def authors(request):
    context_data = {
        'title': 'Авторы',
        'authors': User.objects.filter(is_active=True)
    }
    return render(request, 'users/authors.html', context_data)