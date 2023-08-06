from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Define Work Log category
    """
    list_display=('category', 'category_label')