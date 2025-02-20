from django import forms
from .models import Problema

class ProblemaForm(forms.ModelForm):
    class Meta:
        model = Problema
        fields = ['titulo', 'descripcion', 'enunciado', 'entrada_ejemplo', 'salida_ejemplo', 'entradas_prueba', 'salidas_esperadas', 'tags']
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control", "style": "width: 50%;"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "style": "height: 60px;"}),
            "enunciado": forms.Textarea(attrs={"class": "form-control", "style": "height: 150px;"}),
            "entrada_ejemplo": forms.Textarea(attrs={"class": "form-control", "style": "height: 100px;"}),
            "salida_ejemplo": forms.Textarea(attrs={"class": "form-control", "style": "height: 100px;"}),
            "entradas_prueba": forms.Textarea(attrs={"class": "form-control", "style": "height: 150px;", "id": "id_entradas_prueba"}),
            "salidas_esperadas": forms.Textarea(attrs={"class": "form-control", "style": "height: 150px;", "id": "id_salidas_esperadas"}),
        }

    class Media:
        js = ('js/admin_buttons.js',)  # Carga el script de JavaScript
