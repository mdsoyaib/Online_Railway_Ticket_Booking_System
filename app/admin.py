from django.contrib import admin
from app.models import CustomUser, Station, Feedback, ContactNumber, ContactForm

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Station)
admin.site.register(Feedback)
admin.site.register(ContactNumber)
admin.site.register(ContactForm)

