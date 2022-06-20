from django.urls import path
from Users.views import home, signup, about_us, contact, send_email_contact


urlpatterns = [
    path('', home, name='home'),
    path('signup', signup, name='signup'),
    path('about_us', about_us, name='about_us'),
    path('contact', contact, name='contact'),
    path('send_email_contact', send_email_contact, name='send_email_contact'),
]
