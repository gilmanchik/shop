from django.http import HttpResponse
from django.shortcuts import render

from goods.models import Categories


def index(request):
    categories = Categories.objects.all()
    print(categories)

    context = {
        'title': 'Home - Главная страница',
        'content': 'Магазин мебели HOME',
        'categories': categories,
    }
    return render(request, 'main/index.html', context)


def about(request):
    context = {
        'title': 'Home - Страница о нас',
        'content': 'Страница с информацией о нас',
        'text_on_page': 'Различная информация о нашем магазине'
    }
    return render(request, 'main/about.html', context)
