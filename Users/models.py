from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save


class User(AbstractUser):
    stripe_customer_id = models.CharField(max_length=50)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_picture', null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
