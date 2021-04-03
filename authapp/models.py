from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta
from geekshop.settings import ACTIVATION_KEY_TTL


class Users(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', blank=True, null=True)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_registered = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.username}"

    @property
    def is_activation_key_expired(self):
        return now() - self.activation_key_registered - timedelta(hours=ACTIVATION_KEY_TTL)
