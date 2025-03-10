from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from goods.models import Categories


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Главная страница'
        context['content'] = 'Магазин мебели HOME'
        return context


# def index(request):
#     context = {
#         'title': 'Home - Главная страница',
#         'content': 'Магазин мебели HOME',
#     }
#     return render(request, 'main/index.html', context)

class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Страница о нас'
        context['content'] = 'Страница с информацией о нас'
        context['text_on_page'] = 'Различная информация о нашем магазине'
        return context

# def about(request):
#     context = {
#         'title': 'Home - Страница о нас',
#         'content': 'Страница с информацией о нас',
#         'text_on_page': 'Различная информация о нашем магазине'
#     }
#     return render(request, 'main/about.html', context)
