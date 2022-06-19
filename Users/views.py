from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from Users.forms import SignUpForm
from Productos.views import get_total_items_cart
from Productos.models import Categoria, Producto


def home(request):
    categories = Categoria.objects.all()
    recommended_products = Producto.objects.filter(recomendar=True)
    list_products = []

    for i in range(len(recommended_products)):
        list_products.append(recommended_products[i])

    data = {
        'categories': categories,
        'recommended_products': list_products,
    }

    number_prd_cart, cart, cart_prd = get_total_items_cart(request)
    data['number_prd_cart'] = number_prd_cart
    data['cart'] = cart
    data['cart_prd'] = cart_prd

    return render(request, 'home.html', data)


def signup(request):

    data = {
        'form': SignUpForm()
    }

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
            messages.success(request, 'Usuario creado correctamente')
            return redirect('home')
        else:
            data['form'] = form
            messages.error(request, 'Error al crear el usuario')

    return render(request, 'registration/signup.html', data)
