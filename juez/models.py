from django.db import models

class Problema(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    enunciado = models.TextField(default="Enunciado no disponible")  # Agregamos el enunciado
    entrada_ejemplo = models.TextField(blank=True, null=True)
    salida_ejemplo = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titulo
