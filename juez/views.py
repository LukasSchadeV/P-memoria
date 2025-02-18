from django.shortcuts import render
from .models import Problema

def lista_problemas(request):
    """ Muestra la lista de problemas disponibles """
    problemas = Problema.objects.all()
    return render(request, 'juez/lista_problemas.html', {'problemas': problemas})

def detalle_problema(request, problema_id):
    """ Muestra los detalles de un problema específico """
    problema = Problema.objects.get(id=problema_id)
    return render(request, 'juez/detalle_problema.html', {'problema': problema})
