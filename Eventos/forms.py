from django import forms
from Eventos.models import Evento


class EventoForm(forms.ModelForm):
    nombre = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Nombre')
    descripcion = forms.CharField(max_length=400, widget=forms.Textarea(attrs={'class': 'form-control'}), label='Descripción')
    imagen = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), label='Imagen', required=False)
    texto_boton = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Texto del botón')
    link_to = forms.CharField(max_length=300, widget=forms.URLInput(attrs={'class': 'form-control'}), label='Link de redirección')
    activo = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control'}), label='¿Activo?')

    class Meta:
        model = Evento
        fields = ['nombre', 'descripcion', 'imagen', 'texto_boton', 'link_to', 'activo']
