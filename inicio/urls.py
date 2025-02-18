from django.urls import path
from .views import pagina_inicio, lista_problemas, detalle_problema  # Verifica que estas vistas existan
from .views import iniciar_sesion, cerrar_sesion, registrar_usuario # verificacion para inicio de usario

urlpatterns = [
    path('login/', iniciar_sesion, name='login'),
    path('logout/', cerrar_sesion, name='logout'),
    path('registro/', registrar_usuario, name='registro'),
    path('', pagina_inicio, name='pagina_inicio'),
    path('problemas/', lista_problemas, name='lista_problemas'),
    path('problema/<int:problema_id>/', detalle_problema, name='detalle_problema'),
]
