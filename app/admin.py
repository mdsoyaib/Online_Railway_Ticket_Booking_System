from django.contrib import admin
from app.models import CustomUser, Station, ClassType, Train, Feedback, ContactNumber, ContactForm

# Register your models here.

admin.site.site_header = 'LTTP Admin Panel'

admin.site.register(CustomUser)
# admin.site.register(Station)
@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'place')

admin.site.register(ClassType)

@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ('name', 'nos', 'source', 'destination', 'departure_time',
                    'arrival_time', 'get_class_type')

    def get_class_type(self, obj):
        return "\n".join([c.name for c in obj.class_type.all()])

admin.site.register(Feedback)
admin.site.register(ContactNumber)
admin.site.register(ContactForm)

