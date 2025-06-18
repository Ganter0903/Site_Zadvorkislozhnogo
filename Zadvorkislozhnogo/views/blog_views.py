from django.db.models import Value, CharField
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.urls import reverse
from Zadvorkislozhnogo.models import Blog
from Zadvorkislozhnogo.forms import BlogForm

class BlogListView(ListView):
    model = Blog
    template_name = 'blogs/blog.html'
    context_object_name = 'items'

    def get_queryset(self):
        return Blog.objects.all().order_by('-created_at').annotate(
            content_type=Value("blog", output_field=CharField()),
            model_name=Value("blog", output_field=CharField())
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Блог'
        return context

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'items/item.html'
    context_object_name = 'item'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Блог'
        context['item'].model_name = self.model._meta.model_name
        if self.request.user.is_authenticated:
            context['is_user_liked'] = self.request.user.likes.filter(object_id=self.object.id, content_type__model=self.model._meta.model_name).exists()
        else:
            context['is_user_liked'] = False
        return context

class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'items/item_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новая запись в блоге'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('Zadvorkislozhnogo:blog_detail', kwargs={'pk': self.object.pk})

class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'items/item_confirm_delete.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление блога'
        context['item'].model_name = self.model._meta.model_name
        return context

    def get_success_url(self):
        return reverse('Zadvorkislozhnogo:blogs')