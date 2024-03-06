from django.contrib import admin
from . models import *

# Register your models here.
class catadmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}
admin.site.register(category,catadmin)

class productadmin(admin.ModelAdmin):
    list_display=['name','price','slug','img']
    list_editable = ['price','img','price']
    list_display_links=['name']
    prepopulated_fields={'slug':('name',)}
admin.site.register(product,productadmin)

