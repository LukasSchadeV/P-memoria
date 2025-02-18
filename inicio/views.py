from django.shortcuts import render
from juez.models import Problema  # Asegúrate de que juez está en INSTALLED_APPS

def pagina_inicio(request):
    problemas = Problema.objects.all().order_by('-id')
    return render(request, 'inicio/index.html', {'problemas': problemas})

def lista_problemas(request):
    problemas = Problema.objects.all()
    return render(request, 'inicio/lista_problemas.html', {'problemas': problemas})

def detalle_problema(request, problema_id):
    problema = Problema.objects.get(id=problema_id)
    return render(request, 'inicio/detalle_problema.html', {'problema': problema})
