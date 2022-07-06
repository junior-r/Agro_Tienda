from django import forms
from Productos.models import Categoria, Producto


class CategoriaForm(forms.ModelForm):
    nombre = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Nombre')
    descripcion = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'class': 'form-control'}), label='Descripción', required=False)
    imagen = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), label='Imagen', required=False)

    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'imagen']


class ProductoForm(forms.ModelForm):
    nombre = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Nombre')
    descripcion = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'class': 'form-control'}), label='Descripción')
    precio = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Precio')
    descuento1 = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Precio de Descuento 1')
    descuento2 = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Precio de Descuento 2')
    descuento3 = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Precio de Descuento 3')

    cantidad = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Cantidad')
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), label='Categoría')
    recomendar = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control'}), label='¿Recomendar?', required=False)

    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'descuento1', 'descuento2', 'descuento3', 'cantidad', 'categoria', 'recomendar']
        help_texts = {
            'descuento1': 'Esta cantidad será restada al precio unitario y presentada en la categoría de 2 - 49.',
            'descuento2': 'Esta cantidad será restada al precio unitario y presentada en la categoría de 50 - 99.',
            'descuento3': 'Esta cantidad será restada al precio unitario y presentada en la categoría de 100 en adelante.'
        }
