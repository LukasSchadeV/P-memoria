from django.contrib import admin
from .models import Problema, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

class ProblemaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo')  # Mostrar ID y título como enlace
    search_fields = ('titulo', 'id')  # Permitir búsqueda por ID y título
    list_filter = ('tags',)  # ✅ Ahora solo filtra por tags correctamente
    list_display_links = ('titulo', 'id')  # Hacer el título y ID clickeables

    # ✅ Agregar tags con un widget de selección múltiple
    filter_horizontal = ('tags',)  # Muestra los tags en una caja de selección múltiple horizontal

    fields = ('titulo', 'descripcion', 'enunciado', 'entrada_ejemplo', 'salida_ejemplo', 'entradas_prueba', 'salidas_esperadas', 'tags')

admin.site.register(Problema, ProblemaAdmin)
