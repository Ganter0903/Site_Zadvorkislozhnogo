from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse
from Zadvorkislozhnogo.models import Story
from Zadvorkislozhnogo.forms import StoryForm

class StoryListView(ListView):
    model = Story
    template_name = 'items/items.html'
    context_object_name = 'items'

    def get_queryset(self):
        return Story.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Стихи'
        context['content_type_story'] = True
        return context

class StoryDetailView(DetailView):
    model = Story
    template_name = 'items/item.html'
    context_object_name = 'item'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save(update_fields=['views_count'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Стихотворение'
        return context

class StoryCreateView(CreateView):
    model = Story
    form_class = StoryForm
    template_name = 'items/item_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новый рассказ'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('Zadvorkislozhnogo:story_detail', kwargs={'pk': self.object.pk})