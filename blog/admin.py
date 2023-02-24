from django.contrib import admin
from .models import *

@admin.action(description='فعال کردن')
def make_activate(modeladmin, request, queryset):
    queryset.update(active=True)

@admin.action(description='غیر فعال کردن')
def make_deactivate(modeladmin, request, queryset):
    queryset.update(active=False)

@admin.register(category_blog)
class category_blogAdmin(admin.ModelAdmin):
    list_display=('title','active',)
    list_filter=('active',)
    search_fields=('title',)


#post admin panel
@admin.register(post_blog)
class post_blogAdmin(admin.ModelAdmin):
    list_display=('title', 'active','created_date',)
    list_filter=('active','created_date',)
    search_fields=('title', 'text')
