from django import template
from datetime import datetime, timezone
from django.shortcuts import redirect


register = template.Library()


# this filter has been created to to show cancel booking button if remaining date more than 1 day
@register.filter(name="date")
def date(travel_dt, current_date):
    try:
        result = travel_dt - current_date
        result = str(result)
        time = result.split()
        x = time[0]
        x = int(x)
        return x

    except:
        return redirect('home')

    
# # this filter has been created to to show book button if current date is smaller than travel date
# @register.filter(name="book")
# def book(travel_dt, current_date):
#     try:
#         total = str(travel_dt) + ' ' + str(current_date)
#         pagla = datetime.strptime(total, '%Y-%m-%d %H:%M:%S.%fZ')
#         now = datetime.now(timezone.utc)
#         result = pagla - now
#         print(result)
#         result = str(result)
#         time = result.split()
        
#         nt = time[2].split(":")
#         ns = nt[0]
#         t = int(ns)
#         print(t)

#         d = time[0]
#         d = int(d)
        
#         if (d == 0 and t >= 1) or d > 0:
#             return True
#         else:
#             return False

#     except:
#         return redirect('home')


# this filter has been created to to show book button if current date is smaller than travel date
@register.filter(name="add")
def add(travel_date, travel_time):
    travel_date = str(travel_date)
    travel_time = str(travel_time)
    travel_dt = travel_date + ' ' + travel_time
    # travel_dt = int(travel_dt)
    print(type(travel_dt))
    cd = datetime.now(timezone.utc)
    print(cd)

    return travel_dt



@register.filter(name="book")
def book(travel_dt, current_date):
    try:
        travel_dt = add()

        result = travel_dt - current_date
        result = str(result)
        time = result.split()
        
        nt = time[2].split(":")
        ns = nt[0]
        t = int(ns)
        print(t)

        d = time[0]
        d = int(d)
        
        if (d == 0 and t >= 1) or d > 0:
            return True
        else:
            return False

    except:
        return redirect('home')