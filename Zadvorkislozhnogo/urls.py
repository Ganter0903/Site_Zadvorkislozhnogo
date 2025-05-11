from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('authors/', Authors, name='authors'),
    path('poetry/', poetry, name='poetry'),
    path('stories/', stories, name='stories'),
    path('audiobooks/', audiobooks, name='audiobooks'),
    path('blog/', blog, name='blog'),
    path('profile/', profile, name='profile'),
    path('auth/', auth, name='auth'),
    path('register/', register, name='auth'),
    path('verify/', verify, name='auth'),
    path('forgot_password/', forgot_password, name='auth'),
]