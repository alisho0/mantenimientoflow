from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Suministro(models.Model):
    nombre = models.CharField(max_length=100)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre


class OrdenDeTrabajo(models.Model):
    # tuplas pq el choice reconoce clave valor y bueno, tendrían la misma clave y valor
    PRIORIDAD = [
        ('Baja', 'Baja'),
        ('Media', 'Media'),
        ('Alta', 'Alta')
    ]
    ESTADO = [
        ('Pendiente', 'Pendiente'),
        ('En Progreso', 'En Progreso'),
        ('Cerrada', 'Cerrada')
    ]

    titulo = models.CharField(max_length=100)
    descripcion_falla = models.TextField()
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_cierre_real = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=15, choices=ESTADO, default='Pendiente')
    creador = models.ForeignKey(User, related_name='ordenes_creadas', on_delete=models.CASCADE)
    operario_asignado = models.ForeignKey(User, related_name='ordenes_asignadas', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.titulo


class ConsumoSuministro(models.Model):
    orden_de_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.CASCADE)
    suministro = models.ForeignKey(Suministro, on_delete=models.CASCADE)
    cantidad_usada = models.PositiveIntegerField()
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.suministro.nombre} ({self.cantidad_usada})"
