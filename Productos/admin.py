from django.contrib import admin
from .models import Categoria, Producto
from .forms import CategoriaForm, ProductoForm


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'imagen')
    search_fields = ('nombre',)
    list_per_page = 10
    form = CategoriaForm


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'precio', 'cantidad', 'categoria', 'created_at')
    search_fields = ('nombre',)
    list_filter = ('created_at', 'cantidad', 'categoria')
    list_per_page = 10
    form = ProductoForm


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
