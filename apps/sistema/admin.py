from django.contrib import admin

from apps.sistema.models import Perfil, Estudiante, Docente

# Register your models here.
admin.site.register(Perfil)
admin.site.register(Estudiante)
admin.site.register(Docente)