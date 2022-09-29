from django.contrib import admin
from .models import *

# Register your models here.
class UrlAdmin(admin.ModelAdmin):
    list_display = ('creator', 'link','uuid','created_on')

admin.site.register(Url,UrlAdmin)
 