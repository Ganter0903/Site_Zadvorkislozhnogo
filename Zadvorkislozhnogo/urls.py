from django.urls import path

from .views import *

app_name = 'main'

urlpatterns = [
    path('', index, name='home'),
    path('authors/', Authors, name='authors'),
    path('poetry/', poetry, name='poetry'),
    path('stories/', stories, name='stories'),
    path('audiobooks/', audiobooks, name='audiobooks'),
    path('blog/', blog, name='blog'),
    path('profile/', profile, name='profile'),
    path('auth/', auth, name='auth'),
    path('register/', register, name='register'),
    path('verify/', verify, name='verify'),
    path('forgot_password/', forgot_password, name='forgot_password'),
]