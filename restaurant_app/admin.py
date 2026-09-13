from django.contrib import admin
from .models import Category
from.models import Menu, CartItem, Cart


admin.site.register(CartItem)
admin.site.register(Cart)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'description']
    ordering = ['id']