import string
import secrets

from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from Zadvorkislozhnogo.models import User, Poem

def poems(request):
    context_data = {
        'title': 'Стихи',
        'items': Poem.objects.all()
    }
    return render(request, 'stories.html', context_data)

class PoemListView(ListView):
    model = Poem
    template_name = 'stories.html'
    context_object_name = 'items'

    def get_queryset(self):
        return Poem.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Стихи'
        context['content_type_poem'] = True
        return context

class PoemDetailView(DetailView):
    model = Poem
    template_name = 'article.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Стихотворение'
        return context

class PoemCreateView(CreateView):
    model = Poem
    template_name = 'poem_list.html'
    context_object_name = 'poems'
    paginate_by = 10

    def get_queryset(self):
        return Poem.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Стихи'
        return context

    def get_success_url(self):
        return reverse('poems')