from django import forms
from Eventos.models import Evento


class EventoForm(forms.ModelForm):
    nombre = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Nombre')
    descripcion = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'class': 'form-control'}), label='Descripción')
    imagen = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), label='Imagen', required=False)
    activo = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control'}), label='¿Activo?')

    class Meta:
        model = Evento
        fields = ['nombre', 'descripcion', 'imagen', 'activo']
