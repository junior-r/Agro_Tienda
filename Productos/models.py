from django.core.exceptions import ValidationError
from django.db import models


def save_image_product(instance, filename):
    return 'productos/{}/{}'.format(instance.id, filename)


def save_image_category(instance, filename):
    return 'categorias/{}/{}'.format(instance.id, filename)


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to=save_image_category, blank=True)
    number_prd = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

    def get_number_prd(self):
        return self.producto_set.count()


class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to=save_image_product, blank=True)
    cantidad = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    recomendar = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def clean_descripcion(self):
        if len(self.descripcion) < 5:
            raise ValidationError('La descripción debe tener al menos 5 caracteres')

    def __str__(self):
        return self.nombre

    def get_short_desc(self):
        if len(self.descripcion) > 50:
            return self.descripcion[:50] + '...'
        return self.descripcion

    def get_absolute_url(self):
        host = 'http://localhost:8000'
        return host + '/productos/producto/' + str(self.id)
