from django.shortcuts import render
from .models import Problema

def pagina_inicio(request):
    problemas = Problema.objects.all()  # Obtener todos los problemas creados
    return render(request, 'inicio/index.html', {'problemas': problemas})
