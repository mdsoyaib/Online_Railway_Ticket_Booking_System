from django import template
from datetime import datetime, timezone


register = template.Library()


# this filter has been created to to show cancel booking button if remaining date more than 1 day
@register.filter(name="date")
def date(travel_dt, current_date):
    result = travel_dt - current_date
    result = str(result)
    time = result.split()
    x = time[0]
    x = int(x)

    return x
