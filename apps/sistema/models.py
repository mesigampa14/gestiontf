from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Perfil(models.Model):
    USUARIO_OPCIONES = (
        ('comision', 'Comisión'),
        ('docente', 'Docente'),
        ('estudiante', 'Estudiante')
    )

    SEXO_OPCIONES = (
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.PositiveIntegerField()
    nombre = models.CharField(max_length=250)
    apellido = models.CharField(max_length=250)
    email = models.EmailField()
    nacimiento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=15, choices=SEXO_OPCIONES)
    domicilio = models.CharField(max_length=250)
    tipo_usuario = models.CharField(max_length=15, choices=USUARIO_OPCIONES)

    def __str__(self):
        return f'{self.user.username} - {self.apellido}, {self.nombre} ({self.tipo_usuario})'


class Estudiante(models.Model):
    user = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    matricula = models.IntegerField()

    def __str__(self):
        return f'{self.user.user.username} - {self.user.apellido}, {self.user.nombre} (Matricula: {self.matricula})'


class Docente(models.Model):
    user = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    cuil = models.BigIntegerField()

    def __str__(self):
        return f'{self.user.user.username} - {self.user.apellido}, {self.user.nombre}'
