from django.contrib import admin

from apps.proyecto.models import Proyecto, ProyectoEstudiante, ProyectoDocente


class EstudianteAdmin(admin.ModelAdmin):
    readonly_fields = ('fecha_alta',)


class DocenteAdmin(admin.ModelAdmin):
    readonly_fields = ('fecha_alta',)


# Register your models here.
admin.site.register(Proyecto)
admin.site.register(ProyectoEstudiante, EstudianteAdmin)
admin.site.register(ProyectoDocente, DocenteAdmin)
