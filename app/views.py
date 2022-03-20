from django.shortcuts import render, redirect
from django.views import View
from app.models import CustomUser, Feedback, ContactForm, ContactNumber, Train, Station, ClassType, Booking, BookingDetail, BillingInfo, Payment, Ticket
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from app.forms import TrainForm
from datetime import timezone, datetime, timedelta


# Create your views here.

# homepage view

class Home(View):
    def get(self, request):
        form = TrainForm
        return render(request, 'home.html', {'form': form})

        
# available train page view

class AvailableTrain(View):
    def get(self, request):
        if request.GET:

            rfrom = request.GET.get('rfrom')
            to = request.GET.get('to')
            date = request.GET.get('date')
            ctype = request.GET.get('ctype')
            adult = request.GET.get('pa')
            child = request.GET.get('pc')

            adult = int(adult)
            child = int(child)

            if rfrom == '' or rfrom == 'Select' or to == '' or to == 'Select' \
                    or date == '' or date == 'mm//dd//yyyy' or ctype == '':
                messages.warning(request, 'Please fillup the form properly')
                return redirect('home')

            elif (adult + child) < 1:
                messages.warning(request, 'Please book minimum 1 seat')
                return redirect('home')

            elif (adult + child) > 5:
                messages.warning(request, 'You can book maximum 5 seat')
                return redirect('home')

            else:
                search = Train.objects.filter(source=rfrom, destination=to, class_type=ctype)
                
                source = Station.objects.get(pk=rfrom)
                destination = Station.objects.get(pk=to)
                class_type = ClassType.objects.get(pk=ctype)
                
                return render(request, 'available_train.html', {'search': search, 'source':source, 'destination':destination, 'class_type':class_type})

        else:
            messages.warning(request, 'Find train first to get available train')
            return redirect('home')


#Booking page view

class Bookings(View):
    def get(self, request):
        if request.GET:

            user = request.user
            if user.is_authenticated:
                
                train = request.GET.get('train')
                source = request.GET.get('source')
                destination = request.GET.get('destination')
                date = request.GET.get('date')
                departure = request.GET.get('departure')
                arrival = request.GET.get('arrival')
                tp = request.GET.get('tp')
                pa = request.GET.get('pa')
                pc = request.GET.get('pc')
                ctype = request.GET.get('ctype')
                total_fare = request.GET.get('total_fare')

                fare_each = ClassType.objects.get(name=ctype)

                # this is for booking seat according to train seat capacity

                ticket = Ticket.objects.filter(train_name=train, travel_date=date)
                # if ticket.count() < 30:
                #     print(ticket.count())
                available_seat = 30 - ticket.count()
                print(available_seat)
                tp = int(tp)
                if available_seat >= tp:

                    return render(request, 'booking.html', {'train':train, 'source':source, 'destination':destination, 'date':date, 'departure':departure, 'arrival':arrival, 'tp':tp, 'pa':pa, 'pc':pc, 'ctype':ctype, 'total_fare':total_fare, 'fare_each':fare_each})
                else:
                    messages.warning(request, f"sorry! {available_seat} seat is available for this train. Try again!")
                    return redirect('home')
                
                # this is for booking seat according to train seat capacity (end)
                # else:
                #     messages.warning(request, "sorry! enough seat is not available for this train. Try again!")
                #     return redirect('home')
            else:
                messages.warning(request, "login first to book train")
                return redirect('login')
        else:
            messages.warning(request, 'find a train first!')
            return redirect('home')

    def post(self, request):
        user = request.user

        train = request.POST['train']
        source = request.POST['source']
        destination = request.POST['destination']
        travel_date = request.POST['travel_date']
        travel_time = request.POST['departure']
        arrival = request.POST['arrival']
        nop = request.POST['tp']
        adult = request.POST['pa']
        child = request.POST['pc']
        class_type = request.POST['ctype']
        fpp = request.POST['fpp']
        total_fare = request.POST['total_fare']

        email = request.POST['email']
        phone = request.POST['phone']

        pay_method = request.POST['ptype']
        pay_phone = request.POST['pay_phone']
        trxid = request.POST['trxid']

        # time = Train.objects.get(departure_time=travel_time)
        # travel_time = int(travel_time)
        # time = datetime.strftime(time, "HH:MM[:ss[.uuuuuu]][TZ]")

        # logic for travel_time to store in proper format
        if travel_time == 'midnight':
            travel_time = '0 a.m.'
            time = travel_time.split()
            x = time[0]
            y = time[1]
            x = int(x)
            if not y == 'a.m.':
                x = x + 12
            travel_time = timedelta(hours = x)

        elif travel_time == 'noon':
            travel_time = '12 p.m.'
            time = travel_time.split()
            x = time[0]
            y = time[1]
            x = int(x)
            travel_time = timedelta(hours = x)

        else:
            time = travel_time.split()
            x = time[0]
            y = time[1]
            x = int(x)
            if not y == 'a.m.':
                x = x + 12
            travel_time = timedelta(hours = x)        
        # travel_time logic end
        
        # dt = datetime.strftime("YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]", '2022-04-10 14:30:20')
        # print(dt)

        
        booking = Booking(user=user, travel_dt=str(travel_date)+ ' ' + str(travel_time), travel_date=travel_date)

        booking_detail = BookingDetail(booking=booking, train=train, source=source, destination=destination, travel_date=travel_date, nop=nop, adult=adult, child=child, class_type=class_type, fpp=fpp, total_fare=total_fare, travel_time=str(travel_time), travel_dt=str(travel_date)+ ' ' + str(travel_time))
        
        billing_info = BillingInfo(booking=booking, user=user, email=email, phone=phone)
        
        payment = Payment(booking=booking, user=user, pay_amount=total_fare, pay_method=pay_method, phone=pay_phone, trxid=trxid)
        
        booking.save()
        booking_detail.save()
        billing_info.save()
        payment.save()

        # logic to generate ticket
        nop = int(nop)
        i = 1
        while i <= nop:
            ticket = Ticket(booking=booking, user=user, phone=phone, source=source, destination=destination, departure=str(travel_time), travel_date=travel_date, train_name=train, class_type=class_type, fare=fpp)
            ticket.save()
            i+=1
        # ticket generate logic end
            
        messages.success(request, 'Congratulation! Your booking is successfull')
        return redirect('booking_history')


# booking history page view

class BookingHistory(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            booking = Booking.objects.filter(user=user).order_by('-id')

            current_date = datetime.now(timezone.utc)
            
            return render(request, 'booking_history.html', {'booking':booking, 'current_date':current_date})
        else:
            return redirect('login')


# booking detail page view

class BookingDetails(View):
    def get(self, request, pk):
        user = request.user
        if user.is_authenticated:
            bookings = Booking.objects.get(id=pk)
            if user == bookings.user:
                booking_detail = BookingDetail.objects.get(booking=pk)
                billing = BillingInfo.objects.get(booking=pk)
                payment = Payment.objects.get(booking=pk)
                return render(request, 'booking_detail.html', {'booking_detail':booking_detail, 'billing':billing, 'payment':payment})
            else:
                messages.warning(request, "Invalid booking id!")
                return redirect('booking_history')
        else:
            return redirect('login')


# ticket page view

class Tickets(View):
    def get(self, request, pk):
        user = request.user
        if user.is_authenticated:
            bookings = Booking.objects.get(id=pk)
            if user == bookings.user:
                ticket = Ticket.objects.filter(booking=bookings)
                return render(request, 'ticket.html', {'ticket':ticket, 'bookings':bookings})
            else:
                messages.warning(request, 'Invalid booking id!')
                return redirect('booking_history')
        else:
            return redirect('login')


# cancel booking view

class CancelBooking(View):
    def post(self, request):
        id = request.POST['booking_id']
        Booking.objects.filter(id=id).delete()
        messages.success(request, 'Your booking canceled successfully')
        return redirect(request.META['HTTP_REFERER'])


# signup for user

def signup(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home')
    else:
        if request.method=="POST":
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            phone = request.POST['phone']        
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 != password2:
                messages.warning(request,"Password didn't matched")
                return redirect('signup')
        
            elif username == '':
                messages.warning(request,"Please enter a username")
                return redirect('signup')

            elif first_name == '':
                messages.warning(request,"Please enter first name")
                return redirect('signup')

            elif last_name == '':
                messages.warning(request,"Please enter last name")
                return redirect('signup')

            elif email == '':
                messages.warning(request,"Please enter email address")
                return redirect('signup')

            elif phone == '':
                messages.warning(request,"Please enter phone number")
                return redirect('signup')

            elif password1 == '':
                messages.warning(request,"Please enter password")
                return redirect('signup')

            elif password2 == '':
                messages.warning(request,"Please enter confirm password")
                return redirect('signup')
            
            try:
                if CustomUser.objects.all().get(username=username):
                    messages.warning(request,"username not Available")
                    return redirect('signup')

            except:
                pass
                

            new_user = CustomUser.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, phone=phone, password=password1)
            new_user.is_superuser=False
            new_user.is_staff=False
                
            new_user.save()
            messages.success(request,"Registration Successfull")
            return redirect("login")
        return render(request, 'signup.html')


# login for admin and user

def user_login(request):
    check = request.user
    if check.is_authenticated:
        return redirect('home')
    else:
            
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username,password=password)
            
            if user is not None:
                login(request,user)
                messages.success(request,"successful logged in")
                return redirect('home')
            else:
                messages.warning(request,"Incorrect username or password")
                return redirect('login')

    response = render(request, 'login.html')
    return HttpResponse(response)


# contact page view

class Contact(View):
    def get(self, request):
        contact = ContactNumber.objects.all()
        return render(request, 'contact.html', {'contact': contact})

    def post(self, request):
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        if name == '' or email == '' or message == '':
            messages.warning(request, 'Please fillup all the fields to send message!')
            return redirect('contact')
        
        else:
            form = ContactForm(name=name, email=email, message=message)
            form.save()
            messages.success(request, 'You have successfully sent the message!')  
            return redirect('contact')


# feedback page view

class Feedbacks(View):
    def get(self, request):
        feedback = Feedback.objects.all().order_by('-id')
        return render(request, 'feedback.html', {'feedback': feedback})

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            comment = request.POST['feedback']

            if comment == '':
                messages.warning(request, "please write something first and then submit feedback.")
                return redirect('feedback')
            
            else:
                feedback = Feedback(name=user.first_name + ' ' + user.last_name, feedback=comment)
                feedback.save()
                messages.success(request, 'Thanks for your feedback!')
                return redirect('feedback')

        else:
            messages.warning(request, "Please login first to post feedback.")
            return redirect('feedback')


# verify ticket page view

class VerifyTicket(View):
    def get(self, request):
        trains = Train.objects.all()
        if request.GET:

            train = request.GET.get('train')
            date = request.GET.get('date')
            tid = request.GET.get('tid')

            tid = str(tid)
            date = str(date)

            ticket = None

            try:
                ticket = Ticket.objects.get(id=tid, train_name=train, travel_date=date)
                ticket.id = str(ticket.id)
                ticket.travel_date = str(ticket.travel_date)
                return render(request, 'verify_ticket.html', {'train':trains, 'ticket':ticket})

            except:
                ticket = None
                return render(request, 'verify_ticket.html', {'train':trains, 'ticket':ticket})
            
        else:
            return render(request, 'verify_ticket.html', {'train':trains})

        return render(request, 'verify_ticket.html', {'train':trains})


# profile page view for user

class Profile(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return render(request, 'profile.html')
        else:
            return redirect('login')