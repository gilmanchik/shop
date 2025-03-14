from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

app_name = 'main'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('about/', cache_page(60)(AboutView.as_view()), name='about'),
]