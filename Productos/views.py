import datetime

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect
from django.template.loader import get_template

from Productos.Cart import Cart
from Productos.models import Categoria, Producto, Compra
from django.contrib import messages


def get_total_items_cart(request):
    if 'cart' in request.session.keys():
        cart = Cart(request)

        number_prd_cart = 0
        cart_prd = []
        for item in cart.get_items():
            number_prd_cart += 1
            cart_prd.append(item)

        return number_prd_cart, cart, cart_prd
    else:
        return 0, None, None


def productos(request):
    productos = Producto.objects.all()
    page = request.GET.get('page', 1)
    categories = Categoria.objects.all()

    try:
        paginator = Paginator(productos, 9)
        productos = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': productos,
        'paginator': paginator,
        'categories': categories,
    }

    number_prd_cart, cart, cart_prd  = get_total_items_cart(request)
    data['number_prd_cart'] = number_prd_cart
    data['cart'] = cart
    data['cart_prd'] = cart_prd

    if request.method == 'GET':
        category = request.GET.get('category')
        if category:
            categoria_productos = Producto.objects.filter(categoria_id=int(category))
            categoria = Categoria.objects.get(id=int(category))

            paginator = Paginator(categoria_productos, 9)
            productos = paginator.page(page)
            data['entity'] = productos
            data['paginator'] = paginator
            data['categories'] = categories
            data['result_category'] = categoria_productos
            data['category'] = categoria
            data['category_request'] = int(category)
        else:
            pass

    return render(request, 'productos/productos.html', data)


def detail_producto(request, id):
    producto = Producto.objects.get(id=id)
    categories = Categoria.objects.all()

    data = {
        'producto': producto,
        'categories': categories,
    }

    number_prd_cart, cart, cart_prd = get_total_items_cart(request)
    data['number_prd_cart'] = number_prd_cart
    data['cart'] = cart
    data['cart_prd'] = cart_prd

    return render(request, 'productos/detail_producto.html', data)


def cart(request):
    categories = Categoria.objects.all()

    data = {
        'categories': categories,
    }

    number_prd_cart, cart, cart_prd = get_total_items_cart(request)
    data['number_prd_cart'] = number_prd_cart
    data['cart'] = cart
    data['cart_prd'] = cart_prd

    return render(request, 'productos/cart.html', data)


def add_to_cart(request, id):
    producto = Producto.objects.get(id=id)
    cantidad = request.POST.get('cantidad')

    cart = Cart(request)
    cart_prd = cart.get_items()

    if int(cantidad) > producto.cantidad:
        messages.error(request, 'No hay suficientes unidades en stock')
        return redirect('productos')

    for item in cart_prd:
        if producto.id == item['producto_id']:  # Si el producto ya esta en el carrito
            if int(cantidad) + item['cantidad'] > producto.cantidad:  # Si la cantidad a agregar es mayor a la cantidad en stock
                messages.error(request, 'No hay suficientes unidades en stock')
                return redirect('productos')

    else:
        cart.add(producto, int(cantidad))
        messages.success(request, 'Producto añadido al carrito')
        return redirect('productos')


def remove_from_cart(request, id):
    producto = Producto.objects.get(id=id)
    cart = Cart(request)
    try:
        cart.delete(producto)
        messages.success(request, 'Producto eliminado del carrito')
    except:
        messages.error(request, 'Ha ocurrido un error al eliminar el producto del carrito')
    return redirect('productos')


def clean_cart(request):
    cart = Cart(request)
    try:
        cart.clean()
        messages.success(request, 'Carrito vaciado exitosamente!')
    except Exception as e:
        messages.error(request, 'Ocurrio un error al limpiar el carrito. Intente de nuevo o Contactenos!')
    return redirect('productos')


def increment_prd_cart(request, id):
    producto = Producto.objects.get(id=id)
    cart = Cart(request)

    try:
        cart.add(producto, 1)
    except Exception as e:
        messages.error(request, 'Ocurrió algún error')

    return redirect('cart')


def decrement_prd_cart(request, id):
    producto = Producto.objects.get(id=id)
    cart = Cart(request)

    try:
        cart.sub(producto)
    except Exception as e:
        messages.error(request, 'Ocurrió algún error')

    return redirect('cart')


def datos_envio(request):
    name = request.POST.get('name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    city = request.POST.get('city')
    country = request.POST.get('country')
    dni = request.POST.get('dni')

    return name, last_name, email, phone, address, city, country, dni


def checkout(request):
    categories = Categoria.objects.all()

    data = {
        'categories': categories,
    }

    number_prd_cart, cart, cart_prd = get_total_items_cart(request)
    data['number_prd_cart'] = number_prd_cart
    data['cart'] = cart
    data['cart_prd'] = cart_prd

    if request.method == 'POST':
        name, last_name, email, phone, address, city, country, dni = datos_envio(request)
        request.session['datos_envio'] = {
            'name': name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'address': address,
            'city': city,
            'country': country,
            'dni': dni,
        }
        messages.success(request, 'Datos de envio guardados')
        return redirect('send_method')

    return render(request, 'productos/checkout.html', data)


def send_method(request):
    categories = Categoria.objects.all()

    data = {
        'categories': categories,
    }

    number_prd_cart, cart, cart_prd = get_total_items_cart(request)
    data['number_prd_cart'] = number_prd_cart
    data['cart'] = cart
    data['cart_prd'] = cart_prd

    if request.session['datos_envio']:
        datos_envio = request.session['datos_envio']
        data['datos_envio'] = datos_envio

    if request.method == 'POST':
        method = request.POST.get('method')
        if method:
            request.session['method'] = method
            messages.success(request, 'Metodo de envio guardado')
            return redirect('pago')

    return render(request, 'productos/metodo_envío.html', data)


def pago(request):
    categories = Categoria.objects.all()

    # generar numero aleatorio irrepetible de 5 digitos para el codigo de la transaccion
    import random
    codigo_transaccion = random.randint(10000, 99999)

    data = {
        'categories': categories,
        'codigo_transaccion': codigo_transaccion,
        'fecha': datetime.datetime.now(),
    }

    number_prd_cart, cart, cart_prd = get_total_items_cart(request)
    data['number_prd_cart'] = number_prd_cart
    data['cart'] = cart
    data['cart_prd'] = cart_prd

    if request.session['datos_envio'] and request.session['method']:
        datos_envio = request.session['datos_envio']
        method = request.session['method']
        request.session['codigo_transaccion'] = codigo_transaccion

        data['datos_envio'] = datos_envio
        data['method'] = method

    return render(request, 'productos/pago.html', data)


def confirmar_pago(request):
    categories = Categoria.objects.all()

    data = {
        'categories': categories,
        'fecha': datetime.datetime.now(),
    }

    number_prd_cart, cart, cart_prd = get_total_items_cart(request)
    data['number_prd_cart'] = number_prd_cart
    data['cart'] = cart
    data['cart_prd'] = cart_prd

    if request.session['datos_envio'] and request.session['method'] and request.session['codigo_transaccion']:
        datos_envio = request.session['datos_envio']
        method = request.session['method']
        codigo_transaccion = request.session['codigo_transaccion']

        productos_list = []

        for item in cart_prd:
            for i in cart_prd:
                productos_list.append(i)


        for i in productos_list:
            # Se guarda la compra en la base de datos.
            compra = Compra(
                producto_id=i['producto_id'],
                cantidad=i['cantidad'],
                precio=i['precio'],
                subtotal=cart.get_subtotal(),
                monto_total=i['monto_total'],
                total=cart.get_total_iva(),
                codigo_compra=codigo_transaccion,
            )
            compra.save()

        # Enviar los productos compraddos al mail del usuario.
        name = request.session['datos_envio']['name']
        subject = 'Productos que compraste'
        email_user = request.session['datos_envio']['email']
        message = f'Hola {name}, este es tu comprobante de compra, con esto debes retirar tus productos.'

        data['name'] = name
        data['subject'] = subject
        data['email_user'] = email_user
        data['message'] = message
        data['codigo_compra'] = codigo_transaccion

        template = get_template('productos/send_cart_products.html')
        content = template.render(data)

        email = EmailMultiAlternatives(
            subject,
            message,
            settings.EMAIL_HOST_USER,  # From email
            [email_user]  # To email
        )

        email.attach_alternative(content, 'text/html')
        email.send(fail_silently=False)

        messages.success(request, f'Comprobante de compra enviado al correo {email_user}')

        # Borrar los datos de envío del usuario.
        request.session['datos_envio'] = ''
        method = ''

        return redirect('cart')

    else:
        messages.error(request, 'Ha ocurrido un error al registrar la compra')


