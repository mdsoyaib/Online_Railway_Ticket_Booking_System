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
        return self.name


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


class Booking(models.Model):
    status = (
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Canceled", "Canceled"),
    )
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.PROTECT)
    booking_date = models.DateField(auto_now_add=True, null=True, blank=True)
    booking_time = models.TimeField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(max_length=50, default='Pending', choices=status, auto_created=True, null=True, blank=True)
    travel_date = models.DateField(null=True, blank=True)
    travel_dt = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class BookingDetail(models.Model):
    booking = models.OneToOneField(Booking, null=True, blank=True, on_delete=models.CASCADE)
    train = models.CharField(max_length=255, null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    destination = models.CharField(max_length=255, null=True, blank=True)
    travel_date = models.DateField(null=True, blank=True)
    travel_time = models.TimeField(null=True, blank=True)
    nop = models.PositiveIntegerField(verbose_name=_("Number of Passengers"), null=True, blank=True)
    adult = models.PositiveIntegerField(null=True, blank=True)
    child = models.PositiveIntegerField(null=True, blank=True)
    class_type = models.CharField(max_length=255, null=True, blank=True)
    fpp = models.PositiveIntegerField(verbose_name=_("Fare Per Passenger"), null=True, blank=True)
    total_fare = models.PositiveIntegerField(null=True, blank=True)

    travel_dt = models.DateTimeField(blank=True, null=True)
    booking_dt = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class BillingInfo(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True, blank=True)
    pay_amount = models.PositiveIntegerField(null=True, blank=True)
    pay_method = models.CharField(max_length=25, null=True, blank=True)
    phone = models.CharField(max_length=14, null=True, blank=True)
    trxid = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Transaction Id"))
    status = models.CharField(max_length=50, default='Paid', auto_created=True, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class Ticket(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True, blank=True)
    phone = models.CharField(max_length=14, null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    destination = models.CharField(max_length=255, null=True, blank=True)
    departure = models.TimeField(null=True, blank=True)
    travel_date = models.DateField(null=True, blank=True)
    train_name = models.CharField(max_length=255, null=True, blank=True)
    class_type = models.CharField(max_length=255, null=True, blank=True)
    fare = models.PositiveIntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


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