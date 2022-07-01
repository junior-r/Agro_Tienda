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
    descripcion = models.TextField(max_length=500)
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
        host = 'https://carnetoday.com'
        return host + '/productos/producto/' + str(self.id)

    def get_price5(self):
        if self.cantidad > 5:
            return self.precio * 5
        return f"{self.precio * 5} (No hay suficientes en stock)"

    def get_price50(self):
        if self.cantidad > 50:
            return self.precio * 50
        return f"{self.precio * 50} (No hay suficientes en stock)"

    def get_price100(self):
        if self.cantidad > 100:
            return self.precio * 100
        return f"{self.precio * 100} (No hay suficientes en stock)"


class Compra(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField(default=0)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    codigo_compra = models.CharField(max_length=50)
    estado = models.BooleanField(default=False)

    def __str__(self):
        return self.producto.nombre
