from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('О сайте/', about, name='about'),
]