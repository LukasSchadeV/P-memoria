from django.db import models

class Tag(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Problema(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    enunciado = models.TextField(default="Enunciado no disponible")  
    entrada_ejemplo = models.TextField(blank=True, null=True)  
    salida_ejemplo = models.TextField(blank=True, null=True)  
    ip_creacion = models.GenericIPAddressField(blank=True, null=True)  
    entradas_prueba = models.TextField(help_text="Para diferentes Test usar @@@ como separador")
    salidas_esperadas = models.TextField(help_text="Para diferentes Test usar @@@ como separador")

    # ✅ Relación con Tags corregida
    tags = models.ManyToManyField(Tag, blank=True)  

    def __str__(self):
        return self.titulo