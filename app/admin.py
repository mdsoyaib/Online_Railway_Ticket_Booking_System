from django.contrib import admin
from app.models import CustomUser, Feedback, ContactForm

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Feedback)
admin.site.register(ContactForm)
