import string
import secrets

from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from Zadvorkislozhnogo.models import User, Poem
from Zadvorkislozhnogo.forms import PoemForm

class PoemListView(ListView):
    model = Poem
    template_name = 'items/items.html'
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
    template_name = 'items/item.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Стихотворение'
        return context

class PoemCreateView(CreateView):
    model = Poem
    form_class = PoemForm
    template_name = 'items/item_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новое стихотворение'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('Zadvorkislozhnogo:poem_detail', kwargs={'pk': self.object.pk})