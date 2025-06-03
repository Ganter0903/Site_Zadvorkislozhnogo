from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Value, CharField
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from itertools import chain
from Zadvorkislozhnogo.models import (
    User, Poem, Story, 
    Audiobook, Like, Comment
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