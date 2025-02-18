from django.urls import path
from .views import lista_problemas, detalle_problema

urlpatterns = [
    path('problemas/', lista_problemas, name='lista_problemas'),
    path('problema/<int:problema_id>/', detalle_problema, name='detalle_problema'),  # Ruta de detalle
]
