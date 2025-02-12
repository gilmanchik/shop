from django.urls import path

from .views import *

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('users-cart/', users_cart, name='users_cart'),

]