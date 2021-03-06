from django.urls import path
from Productos.views import productos, detail_producto, cart, add_to_cart, remove_from_cart, decrement_prd_cart, \
    increment_prd_cart, clean_cart, checkout, send_method, pago, confirmar_pago


urlpatterns = [
    path('', productos, name='productos'),
    path('producto/<id>/', detail_producto, name='detail_producto'),
    path('cart/', cart, name='cart'),
    path('add_to_cart/<id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<id>/', remove_from_cart, name='remove_from_cart'),
    path('increment_prd_cart/<id>/', increment_prd_cart, name='increment_prd_cart'),
    path('decrement_prd_cart/<id>/', decrement_prd_cart, name='decrement_prd_cart'),
    path('clean_cart/', clean_cart, name='clean_cart'),
    path('checkout/', checkout, name='checkout'),
    path('send_method/', send_method, name='send_method'),
    path('pago/', pago, name='pago'),
    path('confirmar_pago/', confirmar_pago, name='confirmar_pago'),
]
