from django.contrib import admin
from financial.models import *
from django_json_widget.widgets import JSONEditorWidget
# Register your models here.
#user_offer admin panel
@admin.register(user_offer)
class user_offerAdmin(admin.ModelAdmin):
    list_display=('slug','item','count','count_use','offer_price','active','created_date',)
    list_filter=('active','created_date')
    search_fields=('description','slug')
    ordering=['id','slug']
#User_factor admin panel
@admin.register(User_factor)
class User_factorAdmin(admin.ModelAdmin):
    list_display=('fk_user','items','payment_status','fk_offer','payment_method','payment_date','created_date',)
    list_filter=('created_date','payment_date')
    search_fields=('description','payment_method')
    ordering=['id','payment_method']
    formfield_overrides = {
        # fields.JSONField: {'widget': JSONEditorWidget}, # if django < 3.1
        models.JSONField: {'widget': JSONEditorWidget},
    }
