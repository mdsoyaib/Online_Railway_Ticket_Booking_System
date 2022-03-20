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
# if current train departure time left 1 or more than 1 hour than current time then, book button will be shown
@register.filter(name="add")
def add(travel_date, travel_time):
    travel_date = str(travel_date)
    travel_time = str(travel_time)
    travel_dt = travel_date + ' ' + travel_time
    return travel_dt

@register.filter(name="book")
def book(travel_date, travel_time):

    travel_dt = add(travel_date, travel_time)
    travel_ndt = datetime.strptime(travel_dt, '%Y-%m-%d %H:%M:%S')
    # travel_dt = travel_dt.split()
    # travel_d = travel_dt[0]
    # travel_t = travel_dt[1]

    current_dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_ndt = datetime.strptime(current_dt, '%Y-%m-%d %H:%M:%S')
    # current_dt = str(current_dt)
    # current_x = current_dt.split(".")
    # current_ndt = current_x[0]
    # current_ndt = str(current_ndt)
    # current_xndt = datetime.strptime(current_ndt, '%Y-%m-%d %H:%M:%S')

    # current_dt = str(current_dt)
    # current_dt = current_dt.split()
    # current_d = current_dt[0]
    # current_t = current_dt[1]
    
    # print(f"this is: {travel_ndt} and {current_dt}")

    result = travel_ndt - current_ndt
    print(result)
    result = str(result)
    result = result.split()
    
    try:
        d = result[0]
        d = int(d)
        print(f'this is {d}')
        
        nt = result[2].split(":")
        nth = nt[0]
        t = int(nth)
        print(f'this is {t}')

        if (d >= 0 and t >= 1) or d > 0:
            return True
        else:
            return False
    
    except: 
        nt = result[0].split(":")
        nth = nt[0]
        t = int(nth)
        print(f'except this is {t}')
        if t >= 1:
            return True
        else:
            return False

    # return travel_dt

    # except:
    #     return redirect('home')