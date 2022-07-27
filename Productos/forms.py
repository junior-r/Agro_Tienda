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
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Nombre')
    descripcion = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control'}), label='Descripción')
    precio = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Precio unitario')
    descuento1 = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Precio de Descuento 1')
    descuento2 = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Precio de Descuento 2')
    descuento3 = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Precio de Descuento 3')

    first_number_range_1 = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Número inicial del rango 1')
    last_number_range_1 = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Número límite del rango 1')
    first_number_range_2 = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Número inicial del rango 2')
    last_number_range_2 = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Número límite del rango 2')
    first_number_range_3 = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Número inicial del rango 3')
    last_number_range_3 = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Número límite del rango 3')

    cantidad = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Cantidad')
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), label='Categoría')
    recomendar = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control'}), label='¿Recomendar?', required=False)

    class Meta:
        model = Producto
        fields = "__all__"
        help_texts = {
            'descuento1': 'Esta cantidad será restada al precio unitario y presentada en la categoría de 1 - 49.',
            'descuento2': 'Esta cantidad será restada al precio unitario y presentada en la categoría de 50 - 99.',
            'descuento3': 'Esta cantidad será restada al precio unitario y presentada en la categoría de 100 en adelante.'
        }
