from django.utils.timezone import now
from django.http import HttpResponseNotFound
from django.shortcuts import render
from Zadvorkislozhnogo.models import Subscription, Poem, Story, Audiobook, Genre
from itertools import chain
from datetime import datetime, timedelta
from django.utils.timezone import now
from collections import OrderedDict
from django.db.models import Sum, Q

RU_MONTHS = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']

def chart_view(request):
    
    user = request.user
    if not user.is_authenticated:
        return HttpResponseNotFound(request, 'chart.html', {'title': 'Аналитика', 'error': 'Необходима авторизация'})
    
    # Последние 7 объектов пользователя
    poems = Poem.objects.filter(author=user).only('title', 'views_count', 'created_at')
    stories = Story.objects.filter(author=user).only('title', 'views_count', 'created_at')
    audiobooks = Audiobook.objects.filter(author=user).only('title', 'views_count', 'created_at')
    
    combined = sorted(
        chain(poems, stories, audiobooks),
        key=lambda obj: obj.created_at,
        reverse=True
    )[:7]

    articles = [obj.title for obj in combined]
    views_today = [obj.views_count for obj in combined]
    
    # Последние 5 месяцев, начиная с текущего
    today = now().date().replace(day=1)
    months = OrderedDict()
    for i in range(4, -1, -1):
        month_date = (today - timedelta(days=i * 31)).replace(day=1)
        key = month_date.strftime("%Y-%m")  # '2025-06'
        months[key] = RU_MONTHS[month_date.month - 1]

    # Инициализируем счётчики подписок на пользователя
    subscribers = {key: 0 for key in months}

    # Получаем подписки на текущего пользователя
    subscriptions = Subscription.objects.filter(
        to_user=user,
        created_at__gte=min(datetime.strptime(k, "%Y-%m") for k in months)
    )

    for sub in subscriptions:
        sub_month = sub.created_at.strftime("%Y-%m")
        if sub_month in subscribers:
            subscribers[sub_month] += 1
    
    # Все жанры с хотя бы одной публикацией
    genres = Genre.objects.filter(
        Q(poem__isnull=False) | Q(story__isnull=False) | Q(audiobook__isnull=False)
    ).distinct()

    categories = [genre.title for genre in genres]

    views_month = []
    for genre in genres:
        total_views = (
            (Poem.objects.filter(genre=genre).aggregate(v=Sum('views_count'))['v'] or 0) +
            (Story.objects.filter(genre=genre).aggregate(v=Sum('views_count'))['v'] or 0) +
            (Audiobook.objects.filter(genre=genre).aggregate(v=Sum('views_count'))['v'] or 0)
        )
        views_month.append(total_views)
    
    context = {
        'months': list(months.values()),
        'subscribers': list(subscribers.values()),

        'categories': categories,
        
        'articles': articles,
        'views_today': views_today,
        
        'likes': [80, 50, 60, 30, 40, 20, 10],
        'views_month': views_month,
        
        'title': 'Аналитика',
    }
    return render(request, 'chart.html', context)