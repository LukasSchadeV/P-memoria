from django.db import models

class Problema(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    entrada_ejemplo = models.TextField()
    salida_ejemplo = models.TextField()
    archivo_pruebas = models.FileField(upload_to='pruebas/', blank=True, null=True)

    def __str__(self):
        return self.titulo
