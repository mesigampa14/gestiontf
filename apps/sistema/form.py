from django import forms
from django.forms import DateInput, TextInput

from apps.sistema.models import Perfil, Estudiante, Docente


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ('dni', 'nombre', 'apellido', 'email', 'nacimiento', 'sexo', 'domicilio', 'tipo_usuario')

        widgets = {
            'nacimiento': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'dni': TextInput(attrs={'placeholder': 'Ingrese DNI'}),
            'nombre': TextInput(attrs={'placeholder': 'Ingrese Nombre'}),
            'apellido': TextInput(attrs={'placeholder': 'Ingrese Apellido'}),
            'email': TextInput(attrs={'placeholder': 'Ingrese Correo Electrónico'}),
            'domicilio': TextInput(attrs={'placeholder': 'Ingrese Domicilio'}),
        }


class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ('matricula',)


class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = ('cuil',)
