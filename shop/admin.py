from django.contrib import admin
from .models import *
from adminsortable2.admin import SortableAdminMixin

@admin.action(description='فعال کردن')
def make_activate(modeladmin, request, queryset):
    queryset.update(active=True)

@admin.action(description='غیر فعال کردن')
def make_deactivate(modeladmin, request, queryset):
    queryset.update(active=False)

#attribute_product admin panel
@admin.register(attribute_product)
class attribute_productAdmin(admin.ModelAdmin):
    list_display=('title','unit','active',)
    list_filter=('active',)
    search_fields=('title',)


#product_category admin panel
@admin.register(product_category)
class product_categoryAdmin(admin.ModelAdmin):
    list_display=('title','FK_category','active','created_date',)
    list_filter=('active','created_date',)
    search_fields=('title','active')
    ordering=['id','created_date',]
    actions = [make_activate,make_deactivate]
    

# attr_product inline admin panel
class attr_productInline(admin.TabularInline):
    model=attr_product
    extra=3


#product admin panel
@admin.register(product)
class productAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display=('title', 'active','my_order','created_date',)
    list_filter=('active','created_date',)
    search_fields=('title', 'text')
    ordering = ['my_order']
    inlines=[attr_productInline,]
