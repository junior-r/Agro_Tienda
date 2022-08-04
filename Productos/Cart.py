from Productos.models import ImagenProducto, Producto
import random


class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            self.session['cart'] = {}
            self.cart = self.session['cart']
        else:
            self.cart = cart

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def add(self, producto, cantidad, precio, color):
        id = str(producto.id)
        img_product = ImagenProducto.objects.filter(producto_id=producto.id).first()
        if img_product is not None:
            img = img_product.imagen.url
        else:
            img = ""

        if id not in self.cart.keys():
            # Si el producto no está en el carrito, se agrega con una cantidad = 1
            self.cart[id] = {
                'producto_id': producto.id,
                'imagen': img,
                'nombre': producto.nombre,
                'precio': float(precio),
                'description': producto.get_short_desc(),
                'color': color,
                'cantidad': cantidad,
                'monto_total': round(float(precio) * cantidad, 2)
            }
        else:
            ''' 
                Si el producto ya está en el carrito, se aumenta su cantidad en 1 y el monto total multiplicado 
                por la cantidad
            '''
            self.cart[id]['cantidad'] += cantidad
            self.cart[id]['precio'] = precio
            self.cart[id]['color'] = color
            self.cart[id]['monto_total'] = round(float(self.cart[id]['precio']) * self.cart[id]['cantidad'], 2)
        self.save()

    def delete(self, producto):
        id = str(producto.id)
        if id in self.cart:
            del self.cart[id]
            self.save()

    def sub(self, producto, precio):
        id = str(producto.id)
        if id in self.cart.keys():
            # Si el producto está en el carrito
            self.cart[id]['cantidad'] -= int(1)  # Se resta 1 a la cantidad
            self.cart[id]['precio'] = float(precio)  # Se resta 1 a la cantidad
            self.cart[id]['monto_total'] = round(float(self.cart[id]['precio']) * self.cart[id]['cantidad'], 2)
            if self.cart[id]['cantidad'] <= 0:  # Si la cantidad es menor o igual a 0
                self.delete(producto)
        self.save()

    def get_items(self):
        return self.cart.values()

    def get_subtotal(self):
        subtotal = 0
        for item in self.cart.values():
            subtotal += item['monto_total']
        return round(subtotal, 2)

    def get_iva(self):
        return round(self.get_subtotal() * 0.16, 2)

    def get_total_iva(self):
        subtotal_iva = round(self.get_subtotal() * 0.16 + self.get_subtotal(), 2)
        return subtotal_iva

    def clean(self):
        self.session['cart'] = {}
        self.session.modified = True
