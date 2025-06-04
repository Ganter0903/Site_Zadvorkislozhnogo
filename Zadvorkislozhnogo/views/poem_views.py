from django.db.models import Value, CharField
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse
from Zadvorkislozhnogo.models import Poem
from Zadvorkislozhnogo.forms import PoemForm

class PoemListView(ListView):
    model = Poem
    template_name = 'items/items.html'
    context_object_name = 'items'

    def get_queryset(self):
        return Poem.objects.all().order_by('-created_at').annotate(
            content_type=Value("poem", output_field=CharField()),
            model_name=Value("poem", output_field=CharField())
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Стихи'
        return context

class PoemDetailView(DetailView):
    model = Poem
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
        context['item'].model_name = self.model._meta.model_name
        if self.request.user.is_authenticated:
            context['is_user_liked'] = self.request.user.likes.filter(object_id=self.object.id, content_type__model=self.model._meta.model_name).exists()
        else:
            context['is_user_liked'] = False
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