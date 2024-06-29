from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]
def index(request):
    return render(request, 'Zadvorkislozhnogo/index.html', {'menu': menu, 'title': 'Задворкисложного - официальный сайт'})

def about(request):
    return render(request, 'Zadvorkislozhnogo/about_site.html', {'title': 'О сайте'})

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')