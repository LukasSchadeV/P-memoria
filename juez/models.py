from django.db import models

class Problema(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    enunciado = models.TextField(default="Enunciado no disponible")  # Texto descriptivo del problema
    entrada_ejemplo = models.TextField(blank=True, null=True)  # Entrada de ejemplo (mostrada en el HTML)
    salida_ejemplo = models.TextField(blank=True, null=True)  # Salida de ejemplo (mostrada en el HTML)
    ip_creacion = models.GenericIPAddressField(blank=True, null=True)  # Guardar IP de quien creó el problema
    
    # Campos para verificar el código (no se muestran en el HTML)
    entradas_prueba = models.TextField(help_text="Entradas de prueba separadas por líneas")
    salidas_esperadas = models.TextField(help_text="Salidas esperadas separadas por líneas")

    def __str__(self):
        return self.titulo
