from django.db.models import Count, Value, CharField
from django.http import HttpResponseNotFound
from django.shortcuts import render
from itertools import chain
from Zadvorkislozhnogo.models import User, Poem, Story, Audiobook

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