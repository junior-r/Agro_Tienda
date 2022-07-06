import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.template.loader import get_template

from Users.forms import SignUpForm, ContactForm
from Productos.views import get_total_items_cart
from Productos.models import Categoria, Producto
from Eventos.models import Evento


def contador(request):
    fichero = open("contador.txt", "a+")
    fichero.seek(0)
    contenido = fichero.readline()

    if len(contenido) == 0:
        contenido = "0"
        fichero.write(contenido)
        fichero.close()
        return 0
    else:
        try:
            contador = int(contenido) + 1
            fichero = open("contador.txt", "w")
            fichero.write(str(contador))
            fichero.close()
            return contador
        except:
            print("Error en archivo")
    return redirect('home')


def home(request):
    categories = Categoria.objects.all()
    recommended_products = Producto.objects.filter(recomendar=True)
    prducts = Producto.objects.all()
    evento = Evento.objects.filter(active=True).first()

    list_products = []
    list_catogories = []

    if recommended_products:
        for i in range(len(recommended_products)):
            list_products.append(recommended_products[i])

    if categories:
        counter = 0
        for i in range(len(categories)):
            list_catogories.append(categories[i])
            counter += 1
            if counter >= 4:
                break

    data = {
        'categories': categories,
        'recommended_categories': list_catogories,
        'recommended_products': recommended_products,
        'evento': evento,
        'products': prducts,
        'counter': contador(request)
    }

    number_prd_cart, cart, cart_prd = get_total_items_cart(request)
    data['number_prd_cart'] = number_prd_cart
    data['cart'] = cart
    data['cart_prd'] = cart_prd

    return render(request, 'general/home.html', data)


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


def about_us(request):
    categories = Categoria.objects.all()

    data = {
        'categories': categories,
    }

    number_prd_cart, cart, cart_prd = get_total_items_cart(request)
    data['number_prd_cart'] = number_prd_cart
    data['cart'] = cart
    data['cart_prd'] = cart_prd

    return render(request, 'general/nosotros.html', data)


def contact(request):
    categories = Categoria.objects.all()

    data = {
        'categories': categories,
        'form': ContactForm()
    }

    number_prd_cart, cart, cart_prd = get_total_items_cart(request)
    data['number_prd_cart'] = number_prd_cart
    data['cart'] = cart
    data['cart_prd'] = cart_prd

    return render(request, 'general/contactos.html', data)


def send_email_contact(request):
    """
    Funcion que envia un email al usuario que nos envio el mensaje.

    :param request:

    :return:

    :requirements:
        https://github.com/edwinlunando/django-naomi
        Clave de aplicación en Gmail
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            data = {
                'name': name,
                'subject': subject,
                'email': email,
                'message': message
            }

            template = get_template('general/email_template.html')
            content = template.render(data)

            email = EmailMultiAlternatives(
                subject,
                message,
                settings.EMAIL_HOST_USER,  # From email
                [settings.EMAIL_HOST_USER]  # To email
            )

            email.attach_alternative(content, 'text/html')
            email.send(fail_silently=False)
            messages.success(request, 'Mensaje enviado correctamente.')
        else:
            messages.error(request, 'Algún dato es inválido. Intente de nuevo!')
            print(form.errors)
            return redirect('contact')

    return redirect('contact')


def answers_questions(request):
    categories = Categoria.objects.all()

    data = {
        'categories': categories,
    }

    number_prd_cart, cart, cart_prd = get_total_items_cart(request)
    data['number_prd_cart'] = number_prd_cart
    data['cart'] = cart
    data['cart_prd'] = cart_prd

    return render(request, 'general/answers_questions.html', data)


def page_not_found_404(request, exception):
    return render(request, 'general/page_404.html')
