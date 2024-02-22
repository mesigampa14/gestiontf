from django import forms
from django.forms import DateInput, TextInput, Textarea, Select

from apps.movimiento.models import Movimiento


class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ('observacion',)

        widgets = {
            'observacion': Textarea(attrs={
                'placeholder': 'Ingrese una observación',
                'class': 'form-control',
            }),
        }



class MovPresForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ('etapa', 'estado', 'observacion',)

        widgets = {
            'etapa': Select(attrs={
                'class': 'form-control',
            }),
            'estado': Select(attrs={
                'class': 'form-control',
            }),
            'observacion': Textarea(attrs={
                'placeholder': 'Ingrese una observación',
                'class': 'form-control',
                'rows': '3',
            }),
        }


