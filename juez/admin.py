from django.contrib import admin
from .models import Problema

class ProblemaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo')  # Mostrar ID y título como enlace
    search_fields = ('titulo', 'id')  # Permitir búsqueda por ID y título
    list_filter = ('id', 'titulo')  # Permitir filtrar por ID y título
    fields = ('titulo', 'descripcion', 'enunciado', 'entrada_ejemplo', 'salida_ejemplo', 'entradas_prueba', 'salidas_esperadas')

    list_display_links = ('titulo','id')  # Hacer el título y id un enlace clickeable

admin.site.register(Problema, ProblemaAdmin)
