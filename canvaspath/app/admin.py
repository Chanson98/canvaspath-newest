from django.contrib import admin
from .models import *


# Register your models here.
class AdministratorAdmin(admin.ModelAdmin):
    list_display = ['email', 'password', ]
    search_fields = ('pk', 'email', )

    class Meta:
        model = Administrator

admin.site.register(Administrator, AdministratorAdmin)
