from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100, blank=True, unique=True, null=True)
    phone = models.CharField(verbose_name=_("Mobile phone"), max_length=14, blank=True, null=True, unique=True)
    photo = models.ImageField(verbose_name=_("Photo"), upload_to='users/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"


class Feedback(models.Model):
    name = models.CharField(verbose_name=_("user name"), max_length=255, null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class ContactForm(models.Model):
    name = models.CharField(verbose_name=_("Sender Name"), max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True) 