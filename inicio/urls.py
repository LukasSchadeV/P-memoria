from django.urls import path
from .views import pagina_inicio, lista_problemas, detalle_problema  # Verifica que estas vistas existan

urlpatterns = [
    path('', pagina_inicio, name='pagina_inicio'),
    path('problemas/', lista_problemas, name='lista_problemas'),
    path('problema/<int:problema_id>/', detalle_problema, name='detalle_problema'),
]
