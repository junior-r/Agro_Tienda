from django.shortcuts import render
from Eventos.models import Evento


def eventos(request):
    eventos = Evento.objects.filter(active=True)
    return render(request, 'eventos/eventos.html', {'eventos': eventos})
