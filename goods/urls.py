from django.urls import path

from .views import *

app_name = 'goods'

urlpatterns = [
    path('search/', CatalogView.as_view(), name='search'),
    path('<slug:cat_slug>/', CatalogView.as_view(), name='index'),
    path('product/<slug:product_slug>', ProductView.as_view(), name='product'),
]