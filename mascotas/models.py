from django.db import models

class TipoMascota(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Django crea un id autoincremental automáticamente.

    def __str__(self):
        return self.nombre    

class Mascota(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.PositiveIntegerField()    
    edad_meses = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre