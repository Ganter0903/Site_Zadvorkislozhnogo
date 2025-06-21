import re

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Value, CharField
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from itertools import chain
from Zadvorkislozhnogo.models import (
    User, Poem, Story, 
    Audiobook, Like, Comment,
    About, Document, FAQ, Feedback
)

def index(request):
    
    poems = Poem.objects.all().annotate(content_type=Value('poem', output_field=CharField()))
    stories = Story.objects.all().annotate(content_type=Value('story', output_field=CharField()))
    audiobooks = Audiobook.objects.all().annotate(content_type=Value('audiobook', output_field=CharField()))
    combined_content = list(chain(poems, stories, audiobooks))
    
    context_data = {
        "title": 'Задворки сложного - официальный сайт',
        "popular_authors": User.objects.annotate(
            followers_count=Count('followers')
        ).order_by('-followers_count')[:4],
        "recent_publications": sorted(combined_content, key=lambda x: x.created_at, reverse=True)[:4],
        "top_publications": sorted(combined_content, key=lambda x: x.views_count, reverse=True)[:4],
    }
    return render(request, 'index.html', context_data)

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

@login_required
def toggle_like(request, model_name, object_id):
    if request.method != 'POST':
        return HttpResponseBadRequest('Only POST allowed')

    try:
        content_type = ContentType.objects.get(model=model_name.lower())
        model_class = content_type.model_class()
        obj = get_object_or_404(model_class, id=object_id)
    except ContentType.DoesNotExist:
        raise Http404("Model not found")

    like, created = Like.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=obj.id
    )

    if not created:
        like.delete()

    return HttpResponseRedirect(reverse(f"main:{model_name}_detail", kwargs={'pk': obj.id}))

@login_required
def create_comment(request, model_name, object_id):
    if request.method != 'POST':
        return HttpResponseBadRequest('Only POST allowed')

    try:
        content_type = ContentType.objects.get(model=model_name.lower())
        model_class = content_type.model_class()
        obj = get_object_or_404(model_class, id=object_id)
    except ContentType.DoesNotExist:
        raise Http404("Model not found")

    Comment.objects.create(
        user=request.user,
        content_type=content_type,
        object_id=obj.id,
        text=request.POST.get("text", "")
    )

    return HttpResponseRedirect(reverse(f"main:{model_name}_detail", kwargs={'pk': obj.id}))

def search_view(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return render(request, 'items/items.html', {
                'title': "Строка поиска пуста", 
                'items': []
            })

    try:
        pattern = re.compile(query, re.IGNORECASE)
    except re.error:
        return render(request, 'search/items.html', {
            'title': "Ошибка в строке поиска",
            'items': []
        })

    def filter_queryset(model):
        return [
            obj 
            for obj 
            in model.objects.all().annotate(content_type=Value(
                model._meta.model_name, output_field=CharField()
            )) if pattern.search(obj.title)
        ]

    results = (
        [x for x in filter_queryset(Story)] +
        [x for x in filter_queryset(Poem)] +
        [x for x in filter_queryset(Audiobook)]
    )

    print(results)  # Debugging output
    
    return render(request, 'items/items.html', {
        'title': "Результаты поиска" if results else "Ничего не найдено",
        'items': results
    })

def about_view(request):
    about = About.objects.last()
    if not about:
        raise Http404("About page not found")
    
    return render(request, 'about.html', {
        'title': "О нас",
        'about': about
    })

def faq_list_view(request):
    faqs = FAQ.objects.all()
    if not faqs:
        raise Http404("FAQ page not found")
    
    return render(request, 'faq.html', {
        'title': "Часто задаваемые вопросы",
        'faqs': faqs
    })

def document_list_view(request):
    documents = Document.objects.all()
    if not documents:
        raise Http404("Documents page not found")
    
    return render(request, 'documents.html', {
        'title': "Документы",
        'documents': documents
    })

def feedback_form_view(request):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if not content:
            return render(request, 'feedback_form.html', {
                'title': "Ошибка",
                'error': "Содержание отзыва не может быть пустым."
            })
        
        Feedback.objects.create(user=request.user, content=content)
        return HttpResponseRedirect(reverse('main:feedback_success'))

    return render(request, 'feedback_form.html', {
        'title': "Оставить отзыв"
    })

def feedback_success_view(request):
    return render(request, 'feedback_success.html', {
        'title': "Спасибо за ваш отзыв!"
    })