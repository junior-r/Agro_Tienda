from django.db import models


def save_image_event(instance, filename):
    return 'eventos/{}/{}'.format(instance.id, filename)


class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=400)
    imagen = models.ImageField(upload_to=save_image_event, blank=True, default='eventos/default.jpg')
    texto_boton = models.CharField(max_length=100, null=True, blank=True)
    link = models.URLField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        if self.link:
            return self.link

    class Meta:
        ordering = ['-created_at']
