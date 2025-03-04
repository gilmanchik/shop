from django.contrib import admin

from carts.admin import CartAdminTabular
from .models import User


# admin.site.register(User)

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email']
    search_fields = ['username', 'first_name', 'last_name', 'email']

    inlines = [CartAdminTabular]