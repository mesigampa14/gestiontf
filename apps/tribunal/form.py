from django import forms
from django.forms import DateInput, TextInput, Textarea, Select, IntegerField, FileInput

from apps.tribunal.models import Tribunal


class TribunalForm(forms.ModelForm):
    class Meta:
        model = Tribunal
        fields = ('presidente', 'vocalTitular1', 'vocalTitular2', 'vocalSuplente1', 'vocalSuplente2', 'disposicion_fecha', 'disposicion_numero', 'disposicion_archivo')

        widgets = {
            'presidente': Select(attrs={'class': 'form-control'}),
            'vocalTitular1': Select(attrs={'class': 'form-control'}),
            'vocalTitular2': Select(attrs={'class': 'form-control'}),
            'vocalSuplente1': Select(attrs={'class': 'form-control'}),
            'vocalSuplente2': Select(attrs={'class': 'form-control'}),
            'disposicion_fecha': DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'disposicion_numero': TextInput(attrs={'placeholder': 'Ingrese el número de disposición del tribunal', 'class': 'form-control'}),
            'disposicion_archivo': FileInput(attrs={'class': 'form-control'}),
        }