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
    """
        Función que devuelve datos del carrito.
        The function returns cart data.

        :param: request

        :return:
            * Número de productos en el carrito. -> (int)
            * Objeto carrito. -> (dict)
            * Listado de productos en el carrito. -> (list)
    """

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


def get_categories(request, categories):
    """
        Función que devuelve un listado con 4 diferentes categorías.
        The function returns a list of categories with 4 elements.

        :param:
            * request.
            * categories.
        :return:

    """
    list_catogories = []
    if categories:
        counter = 0
        for i in range(len(categories)):
            list_catogories.append(categories[i])
            counter += 1
            if counter >= 4:
                break
    return list_catogories


def productos(request):
    productos = Producto.objects.all()
    page = request.GET.get('page', 1)
    categories = Categoria.objects.all()
    list_categories = get_categories(request, categories)

    try:
        paginator = Paginator(productos, 12)
        productos = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': productos,
        'paginator': paginator,
        'categories': categories,
        'recommended_categories': list_categories
    }

    number_prd_cart, cart, cart_prd  = get_total_items_cart(request)
    data['number_prd_cart'] = number_prd_cart
    data['cart'] = cart
    data['cart_prd'] = cart_prd

    if request.method == 'GET':
        category = request.GET.get('category')
        if category:
            categoria_productos = Producto.objects.filter(categoria=int(category))
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

    list_categories = get_categories(request, categories)

    data = {
        'producto': producto,
        'categories': categories,
        'recommended_products': recommended_products,
        'recommended_categories': list_categories
    }

    number_prd_cart, cart, cart_prd = get_total_items_cart(request)
    data['number_prd_cart'] = number_prd_cart
    data['cart'] = cart
    data['cart_prd'] = cart_prd

    return render(request, 'productos/detail_producto.html', data)


def cart(request):
    categories = Categoria.objects.all()
    list_categories = get_categories(request, categories)

    data = {
        'categories': categories,
        'recommended_categories': list_categories
    }

    number_prd_cart, cart, cart_prd = get_total_items_cart(request)
    data['number_prd_cart'] = number_prd_cart
    data['cart'] = cart
    data['cart_prd'] = cart_prd

    return render(request, 'productos/cart.html', data)


def get_range_price(request, producto, cantidad, cantidad_cart):
    """
        Función que determina el precio del producto en función de su rango de cantidad.
        Function that determines the price of the product based on its quantity range.

        :params:
            * request.
            * producto (product).
            * cantidad (quantity).
            * cantidad del producto en el carrito (product´s quantity in cart).
        :return:
            Redirección a la página de producto. (redirect to the products page).
    """

    cart = Cart(request)

    if int(cantidad) + int(cantidad_cart) < producto.first_number_range_1:
        # Si la cantidad ingresada + la cantidad guardada es menor al rango más bajo (1), se agrega con su precio uniario.
        cart.add(producto, int(cantidad), float(producto.precio))
    elif (int(cantidad) + int(cantidad_cart)) in range(int(producto.first_number_range_1), int(producto.last_number_range_1) + 1):
        # Si la cantidad ingresada + la cantidad guardada esta en el rango 1
        cart.add(producto, int(cantidad), float(producto.get_descuento1()))
    elif (int(cantidad) + int(cantidad_cart)) in range(int(producto.first_number_range_2), int(producto.last_number_range_2) + 1):
        # Si la cantidad ingresada + la cantidad guardada esta en el rango 2
        cart.add(producto, int(cantidad), float(producto.get_descuento2()))
    elif (int(cantidad) + int(cantidad_cart)) in range(int(producto.first_number_range_3), int(producto.last_number_range_3) + 1):
        # Si la cantidad ingresada + la cantidad guardada esta en el rango 3
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

    for producto_cart in cart_prd:  # Iterar el carrito
        if producto.id == int(producto_cart['producto_id']):
            cantidad_cart = int(producto_cart['cantidad'])
            if cantidad + int(producto_cart['cantidad']) > producto.cantidad:
                messages.error(request, 'No hay suficientes unidades en stock. Intente con menor cantidad!')
                return redirect('detail_producto', id=producto.id)
            else:
                get_range_price(request, producto, cantidad=cantidad, cantidad_cart=cantidad_cart)
                messages.success(request, 'Producto agregado al carrito exitosamente!')
                return redirect('productos')

    get_range_price(request, producto, cantidad, cantidad_cart=0)
    messages.success(request, 'Producto agregado al carrito exitosamente!')
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


def get_price_by_quantity_add(request, product, cant_add, cant_prd_cart):
    cart = Cart(request)

    if int(cant_prd_cart) + cant_add in range(int(product.first_number_range_1), int(product.last_number_range_1) + 1):
        cart.add(product, 1, float(product.get_descuento1()))
        return redirect('cart')
    elif int(cant_prd_cart) + cant_add in range(int(product.first_number_range_2), int(product.last_number_range_2) + 1):
        cart.add(product, 1, float(product.get_descuento2()))
        return redirect('cart')
    elif int(cant_prd_cart) + cant_add in range(int(product.first_number_range_3), int(product.last_number_range_3) + 1):
        cart.add(product, 1, float(product.get_descuento3()))
        return redirect('cart')
    else:
        cart.add(product, 1, float(product.precio))
        return redirect('cart')


def get_price_by_quantity_sub(request, product, cant_prd_cart):
    cart = Cart(request)

    if int(cant_prd_cart) - 1 in range(int(product.first_number_range_1), int(product.last_number_range_1) + 1):
        cart.sub(product, float(product.get_descuento1()))
        return redirect('cart')
    elif int(cant_prd_cart) - 1 in range(int(product.first_number_range_2), int(product.last_number_range_2) + 1):
        cart.sub(product, float(product.get_descuento2()))
        return redirect('cart')
    elif int(cant_prd_cart) - 1 in range(int(product.first_number_range_3), int(product.last_number_range_3) + 1):
        cart.sub(product, float(product.get_descuento3()))
        return redirect('cart')
    else:
        cart.sub(product, float(product.precio))
        return redirect('cart')


def increment_prd_cart(request, id):
    producto = Producto.objects.get(id=id)
    cart = Cart(request)

    try:
        cart_prd = cart.get_items()

        for producto_cart in cart_prd:
            if producto.id == int(producto_cart['producto_id']):
                if int(producto_cart['cantidad']) + 1 > producto.cantidad:
                    messages.error(request, 'Límite de cantidad alcanzado.')
                    return redirect('cart')
                else:
                    cantidad_prd_cart = int(producto_cart['cantidad'])
                    get_price_by_quantity_add(request, producto, 1, cantidad_prd_cart)
                    return redirect('cart')
    except Exception as e:
        messages.error(request, 'Ocurrió algún error')

    return redirect('cart')


def decrement_prd_cart(request, id):
    producto = Producto.objects.get(id=id)
    cart = Cart(request)

    try:
        cart_prd = cart.get_items()
        for producto_cart in cart_prd:
            if producto.id == int(producto_cart['producto_id']):
                cantidad_prd_cart = int(producto_cart['cantidad'])
                get_price_by_quantity_sub(request, producto, cantidad_prd_cart)
                return redirect('cart')
    except Exception as e:
        messages.error(request, 'Ocurrió algún error')

    return redirect('cart')


def datos_envio(request):
    name = request.POST.get('name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    address_mrw = request.POST.get('address_mrw')
    state = request.POST.get('state')
    city = request.POST.get('city')
    country = request.POST.get('country')
    dni = request.POST.get('dni')

    return name, last_name, email, phone, address, address_mrw, state, city, country, dni


def checkout(request):
    categories = Categoria.objects.all()
    list_categories = get_categories(request, categories)

    data = {
        'categories': categories,
        'recommended_categories': list_categories
    }

    number_prd_cart, cart, cart_prd = get_total_items_cart(request)
    data['number_prd_cart'] = number_prd_cart
    data['cart'] = cart
    data['cart_prd'] = cart_prd

    if request.method == 'POST':
        name, last_name, email, phone, address, address_mrw, state, city, country, dni = datos_envio(request)
        request.session['datos_envio'] = {
            'name': name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'address': address,
            'address_mrw': address_mrw,
            'state': state,
            'city': city,
            'country': country,
            'dni': dni,
        }
        return redirect('send_method')

    return render(request, 'productos/checkout.html', data)


def send_method(request):
    categories = Categoria.objects.all()
    list_categories = get_categories(request, categories)

    data = {
        'categories': categories,
        'recommended_categories': list_categories
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
    list_categories = get_categories(request, categories)

    # generar numero aleatorio irrepetible de 5 digitos para el codigo de la transaccion
    import random
    codigo_transaccion = random.randint(10000, 99999)

    data = {
        'categories': categories,
        'codigo_transaccion': codigo_transaccion,
        'fecha': datetime.datetime.now(),
        'recommended_categories': list_categories
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
    list_categories = get_categories(request, categories)

    data = {
        'categories': categories,
        'fecha': datetime.datetime.now(),
        'recommended_categories': list_categories
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


