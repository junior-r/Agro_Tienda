from django.urls import path
from Users.views import home, signup, about_us, contact, send_email_contact, answers_questions


urlpatterns = [
    path('', home, name='home'),
    path('signup', signup, name='signup'),
    path('about_us', about_us, name='about_us'),
    path('contact', contact, name='contact'),
    path('send_email_contact', send_email_contact, name='send_email_contact'),
    path('answers_questions', answers_questions, name='answers_questions'),
]
