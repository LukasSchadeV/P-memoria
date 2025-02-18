from django.contrib import admin
from .models import Problema

class ProblemaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descripcion')  # Solo mostramos título y descripción en la lista
    search_fields = ('titulo',)
    list_filter = ('titulo',)
    fields = ('titulo', 'descripcion', 'enunciado', 'entrada_ejemplo', 'salida_ejemplo', 'entradas_prueba', 'salidas_esperadas')

admin.site.register(Problema, ProblemaAdmin)
