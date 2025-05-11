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
]