from django import forms
from django.forms import DateInput, TextInput, Textarea

from apps.proyecto.models import Proyecto


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ('titulo', 'descripcion', 'presentacion', 'estudiantes', 'director', 'archivos')

        widgets = {
            'presentacion': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'titulo': TextInput(attrs={'placeholder': 'Ingrese el titulo del proyecto'}),
            'descripcion': Textarea(attrs={
                'placeholder': 'Ingrese la descripcion',
                'class': 'form-control'
            }),
        }
