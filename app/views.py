from django.shortcuts import render, redirect
from django.views import View
from app.models import CustomUser, Feedback, ContactForm, ContactNumber, Train, Station, ClassType
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from app.forms import TrainForm


# Create your views here.

# homepage view

class Home(View):
    def get(self, request):
        form = TrainForm
        return render(request, 'home.html', {'form': form})

    # def post(self, request):
    #     source = request.POST['from']
    #     destination = request.POST['to']
    #     date = request.POST['date']
    #     class_type = request.POST['type']
    #     adult = request.POST['pa']
    #     child = request.POST['pc']

    #     adult = int(adult)
    #     child = int(child)

    #     if source == '' or source == 'Select' or destination == '' or destination == 'Select' \
    #             or date == '' or date == 'mm//dd//yyyy' or class_type == '':
    #         messages.warning(request, 'Please fillup the form properly')
    #         return redirect('home')

    #     elif (adult + child) < 1:
    #         messages.warning(request, 'Please book minimum 1 seat')
    #         return redirect('home')

    #     elif (adult + child) > 5:
    #         messages.warning(request, 'You can book maximum 5 seat')
    #         return redirect('home')

    #     else:
    #         print(source, destination, date, class_type, adult, child)
    #         return redirect('home')

    #     return redirect('home')



class AvailableTrain(View):
    def get(self, request):
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


# profile page view for user

class Profile(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return render(request, 'profile.html')
        else:
            return redirect('login')