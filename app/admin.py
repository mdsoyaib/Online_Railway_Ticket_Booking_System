from django.contrib import admin
from app.models import CustomUser, Station, ClassType, Train, Booking, BookingDetail, \
    BillingInfo, Payment, Ticket, Feedback, ContactNumber, ContactForm

# Register your models here.

admin.site.site_header = 'LTTP Admin Panel'


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone')
    search_fields = ('username', 'email')
    list_per_page = 10


# admin.site.register(Station)
@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'place')
    search_fields = ('place',)
    list_per_page = 10


# admin.site.register(ClassType)
@admin.register(ClassType)
class ClassTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ('name', 'nos', 'source', 'destination', 'departure_time',
                    'arrival_time', 'get_class_type')
    list_per_page = 10

    def get_class_type(self, obj):
        return "\n".join([c.name for c in obj.class_type.all()])


# admin.site.register(Booking)
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'booking_date', 'booking_time', 'status', 'travel_dt')
    list_filter = ('status',)
    list_per_page = 10


# admin.site.register(BookingDetail)
@admin.register(BookingDetail)
class BookingDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'train', 'source', 'destination', 'travel_date', 'travel_time', 'nop',
                    'adult', 'child', 'class_type', 'fpp', 'total_fare')
    list_filter = ('class_type', 'train')
    list_per_page = 10


# admin.site.register(BillingInfo)
@admin.register(BillingInfo)
class BillingInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email', 'phone')
    list_per_page = 10


# admin.site.register(Payment)
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'pay_amount', 'pay_method', 'phone', 'trxid', 'status')
    list_filter = ('pay_method',)
    list_per_page = 10


# admin.site.register(Ticket)
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'user', 'phone', 'source', 'destination', 'departure', 'travel_date',
                    'train_name', 'class_type', 'fare')
    list_filter = ('train_name', 'class_type')
    list_per_page = 10


# admin.site.register(Feedback)
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'feedback')
    list_per_page = 10


# admin.site.register(ContactNumber)
@admin.register(ContactNumber)
class ContactNumberAdmin(admin.ModelAdmin):
    list_display = ('station', 'station_phone', 'emergency_center', 'help_desk')
    list_per_page = 10


# admin.site.register(ContactForm)
@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')
    list_per_page = 10
