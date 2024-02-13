from django.db import models

from sistema.models import Estudiante, Docente


# Create your models here.
class Proyecto(models.Model):
    titulo = models.CharField(max_length=300)
    descripcion = models.TextField()
    presentacion = models.DateField(null=True, blank=True)
    archivos = models.FileField(upload_to='apps/proyecto/archivos/', null=True, blank=True)

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
    fecha_baja = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.proyecto} / {self.docente}'


class ProyectoEstudiante(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, default=None)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, default=None)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_baja = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.proyecto} / {self.estudiante}'
