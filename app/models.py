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


class Station(models.Model):
    name = models.CharField(verbose_name=_("Station Name"), max_length=255, null=True, blank=True)
    place = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.name}, {self.place}"


class ClassType(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Train(models.Model):
    name = models.CharField(verbose_name=_("Train Name"), max_length=255, null=True, blank=True)
    nos = models.PositiveIntegerField(verbose_name=_("Number of Seat"), null=True, blank=True)
    source = models.ForeignKey(Station, null=True, blank=True, on_delete=models.PROTECT, related_name='From+')
    destination = models.ForeignKey(Station, null=True, blank=True, on_delete=models.PROTECT, related_name='To+')
    departure_time = models.TimeField(null=True, blank=True)
    arrival_time = models.TimeField(null=True, blank=True)
    class_type = models.ManyToManyField(ClassType, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name


class Feedback(models.Model):
    name = models.CharField(verbose_name=_("user name"), max_length=255, null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class ContactNumber(models.Model):
    station = models.OneToOneField(Station, on_delete=models.CASCADE, null=True, blank=True)
    station_phone = models.CharField(verbose_name=_("Station Phone Number"), max_length=255, null=True, blank=True)
    emergency_center = models.CharField(verbose_name=_("Emergency Center Phone Number"), max_length=255, null=True, blank=True)
    help_desk = models.CharField(verbose_name=_("Help Desk Phone Number"), max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class ContactForm(models.Model):
    name = models.CharField(verbose_name=_("Sender Name"), max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True) 