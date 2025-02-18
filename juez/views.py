from django.shortcuts import render, get_object_or_404
from .models import Problema

def lista_problemas(request):
    """ Muestra la lista de problemas disponibles """
    problemas = Problema.objects.all()
    return render(request, 'juez/lista_problemas.html', {'problemas': problemas})

def detalle_problema(request, problema_id):
    """ Muestra los detalles de un problema específico """
    problema = get_object_or_404(Problema, id=problema_id)  # Si no existe, muestra error 404
    return render(request, 'juez/detalle_problema.html', {'problema': problema})
