from django.contrib import admin
from .models import Categoria, Producto, Compra, ImagenProducto, ColorProduct
from .forms import CategoriaForm, ProductoForm


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'imagen')
    search_fields = ('nombre',)
    list_per_page = 10
    form = CategoriaForm


class ImagenProductoAdmin(admin.TabularInline):
    model = ImagenProducto


class ColorProductAdmin(admin.TabularInline):
    model = ColorProduct


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'cantidad', 'created_at', 'recomendar')
    search_fields = ('nombre',)
    list_filter = ('created_at', 'cantidad', 'categoria')
    list_per_page = 10
    form = ProductoForm
    inlines = [
        ImagenProductoAdmin,
        ColorProductAdmin
    ]


class CompraAdmin(admin.ModelAdmin):
    list_display = ('producto', 'precio', 'cantidad', 'monto_total', 'subtotal', 'created_at', 'estado')
    search_fields = ('codigo_compra',)
    list_filter = ('created_at', 'codigo_compra')
    list_per_page = 10


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Compra, CompraAdmin)
