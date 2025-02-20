from django.contrib import admin
from .models import Problema, Tag
from .forms import ProblemaForm

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

class ProblemaAdmin(admin.ModelAdmin):
    form = ProblemaForm
    list_display = ('id', 'titulo')
    search_fields = ('titulo', 'id')
    list_filter = ('tags',)
    list_display_links = ('titulo', 'id')
    filter_horizontal = ('tags',)

    fieldsets = (
        ("Información General", {"fields": ("titulo", "descripcion")}),
        ("Detalles del Problema", {"fields": ("enunciado",)}),
        ("Ejemplos", {"fields": (("entrada_ejemplo", "salida_ejemplo"),)}),
        ("Casos de Prueba", {
            "fields": (
                ("entradas_prueba", "salidas_esperadas"),
            ),
            "description": "Haz clic en los botones para agregar '@@@' rápidamente.",
        }),
        ("Tags", {"fields": ("tags",)}),
    )

admin.site.register(Problema, ProblemaAdmin)
