from django.db import models

from sistema.models import Estudiante, Docente


# Create your models here.
class Proyecto(models.Model):
    titulo = models.CharField(max_length=300)
    descripcion = models.TextField()
    presentacion = models.DateField(null=True, blank=True)
    estudiantes = models.ManyToManyField(Estudiante)
    director = models.ManyToManyField(Docente)
    archivos = models.FileField(upload_to='apps/proyecto/archivos/', null=True, blank=True)

    def __str__(self):
        return f'{self.titulo}'


class Archivo(models.Model):
    archivo = models.FileField(upload_to='archivos/')
    nombre = models.CharField(max_length=100)


class Director(models.Model):
    CARGO = (
        ('director', 'Director'),
        ('co_director', 'Co-Director'),
        ('asesor', 'Asesor'),
    )
    docente = models.ManyToManyField(Docente)
    cargo = models.CharField(max_length=250, )
    fecha_alta = models.DateTimeField(auto_created=True)
    fecha_baja = models.DateTimeField(auto_now=True)


class Estudiantes(models.Model):
    estudiante = models.ManyToManyField(Estudiante)
    fecha_alta = models.DateTimeField(auto_created=True)
    fecha_baja = models.DateTimeField(auto_now=True)
