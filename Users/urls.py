from django.urls import path
from Users.views import home, signup


urlpatterns = [
    path('', home, name='home'),
    path('signup', signup, name='signup'),
]
