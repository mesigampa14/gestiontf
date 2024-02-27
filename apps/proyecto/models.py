from django.core.validators import FileExtensionValidator
from django.db import models

from apps.sistema.models import Docente, Estudiante
from apps.tribunal.models import Tribunal


# Create your models here.
class Proyecto(models.Model):
    ETAPA = (
        ('evaluacion_comision', 'Evaluación por CSTF'),
        ('evaluacion_tribunal', 'Evaluación por tribunal'),
        ('borrador', 'Presentación del borrador'),
        ('evaluacion_borrador', 'Evaluación del Borrador'),
        ('defensa', 'Defensa del Trabajo Final'),
    )

    ESTADO = (
        ('pendiente', 'Pendiente'),
        ('rechazado', 'Rechazado'),
        ('observado', 'Observado'),
        ('aceptado', 'Aceptado'),
    )
    titulo = models.CharField(max_length=300)
    descripcion = models.TextField()
    presentacion = models.DateField(null=True, blank=True)
    etapa = models.CharField(max_length=250, choices=ETAPA, null=True, blank=True)
    estado = models.CharField(max_length=250, choices=ESTADO, null=True, blank=True)
    archivos = models.FileField(upload_to='apps/proyecto/archivos/', null=True, blank=True)
    tribunal = models.ForeignKey(Tribunal, on_delete=models.CASCADE, blank=True, null=True)
    borrador = models.FileField(upload_to='apps/proyecto/borrador/', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])])
    defensa_fecha = models.DateField(null=True, blank=True)
    defensa_nota = models.IntegerField(null=True,blank=False)

    def __str__(self):
        return f'{self.titulo}'


class Archivo(models.Model):
    archivo = models.FileField(upload_to='archivos/')
    nombre = models.CharField(max_length=100)


class ProyectoDocente(models.Model):
    CARGO = (
        ('director', 'Director'),
        ('co_director', 'Co-Director'),
        ('asesor', 'Asesor'),
    )
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, default=None)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE, default=None)
    cargo = models.CharField(max_length=25, choices=CARGO)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_baja = models.DateTimeField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.proyecto} / {self.docente}'


class ProyectoEstudiante(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, default=None)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, default=None)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_baja = models.DateTimeField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.proyecto} / {self.estudiante}'
