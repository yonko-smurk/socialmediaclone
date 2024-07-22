from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=250, null=False, blank=False)
    last_name = models.CharField(max_length=250, null=False, blank=False)
    email = models.CharField(max_length=250, null=False, blank=False)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, default='')

class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        null=True,
        on_delete=models.CASCADE,
     )
    bio = models.TextField(default='This is the default bio.', blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('accounts:show_profile', args=[str(self.id)])

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()