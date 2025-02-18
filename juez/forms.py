from django import forms
from .models import EnvioCodigo

class EnvioCodigoForm(forms.ModelForm):
    class Meta:
        model = EnvioCodigo
        fields = ['codigo', 'input_file', 'expected_output']
