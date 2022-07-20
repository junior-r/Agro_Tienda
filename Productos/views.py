import datetime
from smtplib import SMTPDataError

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
            try:
                product = Producto.objects.get(id=int(item['producto_id']))
            except:
                product = None

            if product is not None:
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
        paginator = Paginator(productos, 12)
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
    recommended_products = []
    counter = 0
    try:
        productos = Producto.objects.filter(categoria=producto.categoria)
        for i in range(len(productos)):
            recommended_products.append(productos[i])
            if counter >= 4:
                break
    except Exception as e:
        productos = Producto.objects.filter(categoria=categories.first())
        for i in range(len(productos)):
            recommended_products.append(productos[i])
            if counter >= 4:
                break

    data = {
        'producto': producto,
        'categories': categories,
        'recommended_products': recommended_products
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


def get_range_price(request, producto, cantidad, cantidad_cart):
    cart = Cart(request)
    if (int(cantidad) + int(cantidad_cart)) == 1:
        # Si la cantidad ingresada + la cantidad guardada es = 1
        cart.add(producto, int(cantidad), float(producto.precio))
    elif (int(cantidad) + int(cantidad_cart)) in range(1, 49+1):
        # Si la cantidad ingresada + la cantidad guardada esta en el rango 2 - 49
        cart.add(producto, int(cantidad), float(producto.get_descuento1()))
    elif (int(cantidad) + int(cantidad_cart)) in range(50, 99+1):
        # Si la cantidad ingresada + la cantidad guardada esta en el rango 50 - 99
        cart.add(producto, int(cantidad), float(producto.get_descuento2()))
    elif (int(cantidad) + int(cantidad_cart)) >= 100:
        # Si la cantidad ingresada + la cantidad guardada es >= 100
        cart.add(producto, int(cantidad), float(producto.get_descuento3()))
    else:
        messages.error(request, 'Cantidad inválida, intente de nuevo!')
        return redirect('productos')


def add_to_cart(request, id):
    producto = Producto.objects.get(id=id)
    cantidad = request.POST.get('cantidad')
    cantidad = int(cantidad)

    cart = Cart(request)
    cart_prd = cart.get_items()
    if cantidad > producto.cantidad:
        messages.error(request, 'No hay suficientes unidades en stock. Intente con menor cantidad!')
    if cantidad <= 0:
        messages.error(request, 'Cantidad inválida, intente de nuevo!')
        return redirect('detail_producto', id=producto.id)

    if cart_prd:  # Si hay productos en el carrito
        for producto_cart in cart_prd:  # Iterar el carrito
            if producto.id == int(producto_cart['producto_id']):  # Si el producto está en el carrito
                cantidad_cart = int(producto_cart['cantidad'])
                if cantidad + int(producto_cart['cantidad']) > producto.cantidad:
                    messages.error(request, 'No hay suficientes unidades en stock. Intente con menor cantidad!')
                    return redirect('detail_producto', id=producto.id)
                else:
                    get_range_price(request, producto, cantidad=cantidad, cantidad_cart=cantidad_cart)
                    messages.success(request, 'Producto agregado al carrito exitosamente!')
                    return redirect('productos')
            else:
                get_range_price(request, producto, cantidad, cantidad_cart=0)
                messages.success(request, 'Producto agregado al carrito exitosamente!')
                return redirect('productos')
    else:
        get_range_price(request, producto, cantidad, cantidad_cart=0)
        messages.success(request, 'Producto agregado al carrito exitosamente!')
        return redirect('productos')

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
        cart.add(producto, 1, int(producto.precio))
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
    state = request.POST.get('state')
    city = request.POST.get('city')
    country = request.POST.get('country')
    dni = request.POST.get('dni')

    return name, last_name, email, phone, address, state, city, country, dni


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
        name, last_name, email, phone, address, state, city, country, dni = datos_envio(request)
        request.session['datos_envio'] = {
            'name': name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'address': address,
            'state': state,
            'city': city,
            'country': country,
            'dni': dni,
        }
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
        subject = 'Productos comprados'
        email_user = request.session['datos_envio']['email']
        message_user = f'Hola {name}, este es tu comprobante de compra, con esto debes retirar tus productos.'
        message_admin = f'Le vendiste productos a {name}'

        data['name'] = name
        data['subject'] = subject
        data['email_user'] = email_user
        data['message'] = message_user
        data['message_admin'] = message_admin
        data['codigo_compra'] = codigo_transaccion
        data['datos_envio_user'] = datos_envio
        data['method'] = method

        template_user = get_template('productos/send_cart_products.html')
        template_admin = get_template('productos/send_cart_products_admin.html')
        content_user = template_user.render(data)
        content_admin = template_admin.render(data)

        #  Email que será enviado al usuario.
        email = EmailMultiAlternatives(
            subject,
            message_user,
            settings.EMAIL_HOST_USER,  # From email
            [email_user]  # To email
        )

        #  Email que será enviado al administrador.
        email_admin = EmailMultiAlternatives(
            subject,
            message_admin,
            settings.EMAIL_HOST_USER,  # From email
            [settings.EMAIL_HOST_USER]  # To email
        )

        try:
            email.attach_alternative(content_user, 'text/html')
            email_admin.attach_alternative(content_admin, 'text/html')

            email.send(fail_silently=False)
            email_admin.send(fail_silently=False)
            messages.success(request, f'Comprobante de compra enviado al correo {email_user}')
        except SMTPDataError as daily_quote:
            messages.error(request,
                           'En estos momentos no se puede enviar su correo. Porfavor comunicate a nuestro WhatsApp para completar tu orden!')
            return redirect('cart')
        except Exception as e:
            messages.error(request, 'No se pudo enviar su orden, intente de nuevo!')
            return redirect('cart')


        # Borrar los datos de envío del usuario.
        request.session['datos_envio'] = ''
        method = ''

        return redirect('cart')

    else:
        messages.error(request, 'Ha ocurrido un error al registrar la compra')


