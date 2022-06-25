from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.template.loader import get_template

from Users.forms import SignUpForm
from Productos.views import get_total_items_cart
from Productos.models import Categoria, Producto
from Eventos.models import Evento


def home(request):
    categories = Categoria.objects.all()
    recommended_products = Producto.objects.filter(recomendar=True)
    evento = Evento.objects.filter(active=True).first()

    list_products = []

    if recommended_products:
        count = 0
        for i in range(len(recommended_products)):
            list_products.append(recommended_products[i])
            count += 1
            if count == 3:
                break

    data = {
        'categories': categories,
        'recommended_products': list_products,
        'evento': evento
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
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        email = request.POST.get('email')
        message = request.POST.get('message')

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
