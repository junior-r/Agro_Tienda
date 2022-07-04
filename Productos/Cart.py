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

    def add(self, producto, cantidad, precio):
        id = str(producto.id)
        if id not in self.cart.keys():
            # Si el producto no está en el carrito, se agrega con una cantidad = 1
            self.cart[id] = {
                'producto_id': producto.id,
                'imagen': producto.imagen.url,
                'nombre': producto.nombre,
                'precio': float(precio),
                'description': producto.descripcion,
                'cantidad': cantidad,
                'monto_total': float(precio) * cantidad
            }
        else:
            ''' 
                Si el producto ya está en el carrito, se aumenta su cantidad en 1 y el monto total multiplicado 
                por la cantidad
            '''

            self.cart[id]['cantidad'] += cantidad
            self.cart[id]['precio'] = precio
            self.cart[id]['monto_total'] = float(self.cart[id]['precio']) * self.cart[id]['cantidad']
        self.save()

    def delete(self, producto):
        id = str(producto.id)
        if id in self.cart:
            del self.cart[id]
            self.save()

    def sub(self, producto):
        id = str(producto.id)
        if id in self.cart.keys():
            # Si el producto está en el carrito
            self.cart[id]['cantidad'] -= int(1) # Se resta 1 a la cantidad
            self.cart[id]['monto_total'] -= float(producto.precio) # Se resta el precio del producto
            if self.cart[id]['cantidad'] <= 0: # Si la cantidad es menor o igual a 0
                self.delete(producto)
        self.save()

    def get_items(self):
        return self.cart.values()

    def get_subtotal(self):
        subtotal = 0
        for item in self.cart.values():
            subtotal += item['monto_total']
        return subtotal

    def get_iva(self):
        return self.get_subtotal() * 0.16

    def get_total_iva(self):
        return self.get_subtotal() * 0.16 + self.get_subtotal()

    def clean(self):
        self.session['cart'] = {}
        self.session.modified = True
