from django import forms
from django.forms import DateInput, TextInput, Textarea, SelectMultiple

from apps.movimiento.models import Movimiento


class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ('observacion',)

        widgets = {
            'observacion': Textarea(attrs={
                'placeholder': 'Ingrese una observación',
                'class': 'form-control'
            }),
        }