from django import forms
from django.forms import DateInput, TextInput, Textarea, Select

from apps.proyecto.models import Proyecto, ProyectoEstudiante, ProyectoDocente


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ('titulo', 'descripcion', 'presentacion', 'archivos')

        widgets = {
            'presentacion': DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'titulo': TextInput(attrs={'placeholder': 'Ingrese el titulo del proyecto', 'class': 'form-control'}),
            'descripcion': Textarea(attrs={
                'placeholder': 'Ingrese la descripcion',
                'class': 'form-control'
            }),
        }


class ProyectoEstudianteForm(forms.ModelForm):
    class Meta:
        model = ProyectoEstudiante
        fields = ('estudiante',)

        widgets = {
            'estudiante': Select(),
        }


class ProyectoDocenteForm(forms.ModelForm):
    class Meta:
        model = ProyectoDocente
        fields = ('docente',)
