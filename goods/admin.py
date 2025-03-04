from django.contrib import admin

from .models import *


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'quantity', 'price', 'discount']
    list_editable = ['discount']
    search_fields = ['name', 'description']
    list_filter = ['discount', 'quantity', 'category']
    fields = [
        'name',
        'category',
        'slug',
        'description',
        'image',
        ('price', 'discount'),
        'quantity'
    ]