from django.shortcuts import render, redirect
from juez.models import Problema, Tag  # Asegúrate de que juez está en INSTALLED_APPS
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistroForm  # Importamos el formulario actualizado

def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('pagina_inicio')  # Redirige a la página principal
    else:
        form = AuthenticationForm()
    
    return render(request, 'inicio/login.html', {'form': form})

def cerrar_sesion(request):
    logout(request)
    return redirect('pagina_inicio')

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Iniciar sesión automáticamente
            return redirect('pagina_inicio')
    else:
        form = RegistroForm()
    
    return render(request, 'inicio/registro.html', {'form': form})

def pagina_inicio(request):
    """ Muestra la lista de problemas con opción de búsqueda y filtro por tags """
    query = request.GET.get("q", "").strip()
    tag_filter = request.GET.get("tag", "").strip()

    problemas = Problema.objects.all().order_by('-id')
    
    # Filtrar por título si hay búsqueda
    if query:
        problemas = problemas.filter(titulo__icontains=query)

    # Filtrar por tag si se seleccionó uno
    if tag_filter:
        problemas = problemas.filter(tags__nombre__iexact=tag_filter)

    tags = Tag.objects.all()
    
    return render(request, 'inicio/index.html', {'problemas': problemas, 'tags': tags, 'query': query, 'tag_filter': tag_filter})

def lista_problemas(request):
    problemas = Problema.objects.all()
    return render(request, 'inicio/lista_problemas.html', {'problemas': problemas})

def detalle_problema(request, problema_id):
    problema = Problema.objects.get(id=problema_id)
    return render(request, 'inicio/detalle_problema.html', {'problema': problema})
