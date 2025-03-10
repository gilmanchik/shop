from django.urls import path

from .views import *

app_name = 'orders'

urlpatterns = [
    path('create-order/', CreateOrderView.as_view(), name='create_order')
]