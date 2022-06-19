from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect

from Productos.Cart import Cart
from Productos.models import Categoria, Producto
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

    data = {
        'producto': producto,
    }

    number_prd_cart, cart, cart_prd = get_total_items_cart(request)
    data['number_prd_cart'] = number_prd_cart
    data['cart'] = cart
    data['cart_prd'] = cart_prd

    return render(request, 'productos/detail_producto.html', data)


def cart(request):
        data = {}

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
