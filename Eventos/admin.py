from django.contrib import admin
from Eventos.models import Evento
from Eventos.forms import EventoForm


class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'created_at', 'active')
    list_filter = ('created_at', 'active')
    search_fields = ('nombre', 'descripcion')
    ordering = ['-created_at']
    form = EventoForm


admin.site.register(Evento, EventoAdmin)
