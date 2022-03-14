"""lttp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import Home, AvailableTrain, user_login, signup, Contact, Feedbacks, Profile, Bookings, BookingHistory, BookingDetails, Tickets, CancelBooking, VerifyTicket
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name="home"),
    path('available_train', AvailableTrain.as_view(), name="available_train"),
    path('booking', Bookings.as_view(), name='booking'),
    path('booking_history', BookingHistory.as_view(), name="booking_history"),
    path('booking_history/booking_detail/<int:pk>', BookingDetails.as_view(), name="booking_detail"),
    path('booking_history/ticket/<int:pk>', Tickets.as_view(), name="ticket"),
    path('cancel_booking', CancelBooking.as_view(), name="cancel_booking"),
    
    path('contact', Contact.as_view(), name="contact"),
    path('feedback', Feedbacks.as_view(), name="feedback"),
    path('verify_ticket', VerifyTicket.as_view(), name="verify_ticket"),

    path('login', user_login, name="login"),
    path('signup', signup, name="signup"),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),

    path('profile', Profile.as_view(), name="profile"),
]
