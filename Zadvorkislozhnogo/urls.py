from django.urls import path

from .views import *

app_name = 'main'

urlpatterns = [
    path('', index, name='home'),
    path('authors/', authors, name='authors'),
    path('author_profile/<int:pk>/', author_profile, name='author_profile'),
    path('poetry/', poetry, name='poetry'),
    path('stories/', stories, name='stories'),
    path('audiobooks/', audiobooks, name='audiobooks'),
    path('blog/', blog, name='blog'),
    path('profile/', profile, name='profile'),
    path('auth/', login_view, name='auth'),
    path('register/', register_view, name='register'),
    path('verify/<uidb64>/<token>/', verify_email, name='verify_email'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('chart/', chart_view, name='chart'),
    path('article/', article, name='article'),
    path('logout/', logout_view, name='logout'),
]