from django.core.exceptions import ValidationError
from django.db import models

from Agro_Tienda import settings


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

    def get_imagen(self):
        if self.imagen:
            return f'{settings.MEDIA_URL}{self.imagen}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def get_number_prd(self):
        return self.producto_set.count()


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=1000)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descuento1 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    descuento2 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    descuento3 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)

    first_number_range_1 = models.IntegerField(default=0, null=True, blank=True)
    last_number_range_1 = models.IntegerField(default=0, null=True, blank=True)
    first_number_range_2 = models.IntegerField(default=0, null=True, blank=True)
    last_number_range_2 = models.IntegerField(default=0, null=True, blank=True)
    first_number_range_3 = models.IntegerField(default=0, null=True, blank=True)
    last_number_range_3 = models.IntegerField(default=0, null=True, blank=True)

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
        host = 'https://agrovenca.com'
        return host + '/productos/producto/' + str(self.id)

    def get_price(self):
        return self.precio

    def get_descuento1(self):
        if self.descuento1:
            if self.cantidad >= self.first_number_range_1:
                return self.descuento1
            else:
                return f"{self.precio - self.descuento1} (No hay suficientes en stock)"
        else:
            return self.precio

    def get_descuento2(self):
        if self.descuento2:
            if self.cantidad >= self.first_number_range_2:
                return self.descuento2
            else:
                return f"{self.precio - self.descuento2} (No hay suficientes en stock)"
        else:
            return self.get_descuento1()

    def get_descuento3(self):
        if self.descuento3:
            if self.cantidad >= self.descuento3:
                return self.descuento3
            else:
                return f"{self.precio - self.descuento3} (No hay suficientes en stock)"
        else:
            return self.get_descuento2()


class ImagenProducto(models.Model):
    imagen = models.ImageField(upload_to=save_image_product)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="imagenes")


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
