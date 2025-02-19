from django.db import models

class Tag(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Problema(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    enunciado = models.TextField(default="Enunciado no disponible")  
    entrada_ejemplo = models.TextField(blank=True, null=True)  
    salida_ejemplo = models.TextField(blank=True, null=True)  
    ip_creacion = models.GenericIPAddressField(blank=True, null=True)  
    entradas_prueba = models.TextField(help_text="Entradas de prueba separadas por líneas")
    salidas_esperadas = models.TextField(help_text="Salidas esperadas separadas por líneas")

    # ✅ Relación con Tags corregida
    tags = models.ManyToManyField(Tag, blank=True)  

    def __str__(self):
        return self.titulo
