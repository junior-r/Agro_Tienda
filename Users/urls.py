from django.urls import path
from Users.views import home, signup, about_us


urlpatterns = [
    path('', home, name='home'),
    path('signup', signup, name='signup'),
    path('about_us', about_us, name='about_us'),
]
