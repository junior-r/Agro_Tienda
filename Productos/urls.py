from django.urls import path
from Productos.views import productos, detail_producto, cart, add_to_cart, remove_from_cart


urlpatterns = [
    path('', productos, name='productos'),
    path('producto/<id>/', detail_producto, name='detail_producto'),
    path('cart/', cart, name='cart'),
    path('add_to_cart/<id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<id>/', remove_from_cart, name='remove_from_cart'),

]
