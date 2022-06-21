"""Agro_Tienda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from Users.views import page_not_found_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Users.urls'), name='users'),
    path('productos/', include('Productos.urls'), name='productos'),
    path('eventos/', include('Eventos.urls'), name='eventos'),
    path('accounts/', include('django.contrib.auth.urls')),
]

handler404 = page_not_found_404

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
