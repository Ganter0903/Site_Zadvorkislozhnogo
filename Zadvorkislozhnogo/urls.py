from django.urls import path

from .views import (
    index, authors, author_profile,
    stories, audiobooks, blog, 
    PoemListView, PoemDetailView, PoemCreateView,
    profile, login_view, register_view, verify_email,
    forgot_password, chart_view, article, logout_view 
)

app_name = 'main'

urlpatterns = [
    path('', index, name='home'),
    path('authors/', authors, name='authors'),
    path('author_profile/<int:pk>/', author_profile, name='author_profile'),
    
    path('stories/', stories, name='stories'),
    path('audiobooks/', audiobooks, name='audiobooks'),
    path('blog/', blog, name='blog'),

    path('poems/', PoemListView.as_view(), name='poems'),
    path('poems/<int:pk>/', PoemDetailView.as_view(), name='poem_detail'),
    path('poems/create/', PoemCreateView.as_view(), name='poem_create'),
    
    path('profile/', profile, name='profile'),
    path('auth/', login_view, name='auth'),
    path('register/', register_view, name='register'),
    path('verify/<uidb64>/<token>/', verify_email, name='verify_email'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    
    path('chart/', chart_view, name='chart'),
    path('article/', article, name='article'),
    path('logout/', logout_view, name='logout'),
]