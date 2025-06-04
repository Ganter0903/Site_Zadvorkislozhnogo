from django.urls import path

from .views import (
    index, authors, author_profile, blog,
    AudiobookListView, AudiobookDetailView, AudiobookCreateView,
    StoryListView, StoryDetailView, StoryCreateView, 
    PoemListView, PoemDetailView, PoemCreateView,
    toggle_like, create_comment,
    profile, login_view, register_view, verify_email, EditProfile, toggle_subscription, my_subscriptions,
    forgot_password, chart_view, logout_view, search_view
)

app_name = 'main'

urlpatterns = [
    path('', index, name='home'),
    
    path('search/', search_view, name='search'),
    
    path('blog/', blog, name='blog'),

    path('stories/', StoryListView.as_view(), name='stories'),
    path('stories/<int:pk>/', StoryDetailView.as_view(), name='story_detail'),
    path('stories/create/', StoryCreateView.as_view(), name='story_create'),

    path('poems/', PoemListView.as_view(), name='poems'),
    path('poems/<int:pk>/', PoemDetailView.as_view(), name='poem_detail'),
    path('poems/create/', PoemCreateView.as_view(), name='poem_create'),
    
    path('audiobooks/', AudiobookListView.as_view(), name='audiobooks'),
    path('audiobooks/<int:pk>/', AudiobookDetailView.as_view(), name='audiobook_detail'),
    path('audiobooks/create/', AudiobookCreateView.as_view(), name='audiobook_create'),
    
    path('profile/', profile, name='profile'),
    path('auth/', login_view, name='auth'),
    path('register/', register_view, name='register'),
    path('verify/<uidb64>/<token>/', verify_email, name='verify_email'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('logout/', logout_view, name='logout'),
    path('profile/edit/', EditProfile.as_view(), name='edit_profile'),
    
    path('authors/', authors, name='authors'),
    path('author_profile/<int:pk>/', author_profile, name='author_profile'),
    
    path('subscribe/<int:user_id>/', toggle_subscription, name='toggle_subscription'),
    path('subscriptions/', my_subscriptions, name="my_subscriptions"),
    
    path('chart/', chart_view, name='chart'),
    
    path('<str:model_name>/<int:object_id>/like/', toggle_like, name='toggle_like'),
    path('<str:model_name>/<int:object_id>/comment/', create_comment, name='create_comment'),
]