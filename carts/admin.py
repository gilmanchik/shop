from django.contrib import admin

from .models import Cart


# admin.site.register(Cart)

class CartAdminTabular(admin.TabularInline):
    model = Cart
    fields = 'products', 'quantity', 'created_timestamp'
    search_fields = 'products', 'quantity', 'created_timestamp'
    readonly_fields = 'created_timestamp',
    extra = 2


@admin.register(Cart)
class AdminCart(admin.ModelAdmin):
    list_display = ['user', 'products', 'quantity', 'created_timestamp']
    list_filter = ['created_timestamp', 'user', 'products']
