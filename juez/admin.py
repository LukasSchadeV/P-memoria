from django.contrib import admin
from .models import Problema

class ProblemaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descripcion')  # Solo mostramos título y descripción en la lista
    search_fields = ('titulo',)
    list_filter = ('titulo',)

admin.site.register(Problema, ProblemaAdmin)
