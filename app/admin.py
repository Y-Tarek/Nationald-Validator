from django.contrib import admin
from app.models import *

class ServiceAdmin(admin.ModelAdmin):
    readonly_fields = ['public_key','private_key']

admin.site.register(Service,ServiceAdmin)
admin.site.register(Transaction)

# Register your models here.
