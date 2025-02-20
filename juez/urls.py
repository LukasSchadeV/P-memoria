from django.urls import path
from .views import lista_problemas, detalle_problema, execute_c_code, submit_c_code, autocomplete_problemas

urlpatterns = [
    path('problemas/', lista_problemas, name='lista_problemas'),
    path('problema/<int:problema_id>/', detalle_problema, name='detalle_problema'),
    path('problema/<int:problema_id>/execute/', execute_c_code, name="execute_c_code"),
    path('problema/<int:problema_id>/submit/', submit_c_code, name="submit_c_code"),
    path('autocomplete/', autocomplete_problemas, name='autocomplete_problemas'),
]
