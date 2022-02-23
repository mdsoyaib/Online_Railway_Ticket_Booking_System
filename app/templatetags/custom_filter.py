from django import template
from datetime import datetime, date

register = template.Library()


@register.filter(name="passengers")
def passengers(adult, child):
    adult = request.GET.pa
    child = request.GET.pc
    return adult + child


@register.filter(name="multiply")
def multiply(passengers, price):
    price = request.GET.ctype.price
    return passengers * price

# this filter is for getting duration between departure time to arrival time
@register.filter(name="duration")
def duration(departure, arrival):
    sub = datetime.combine(date.min, departure) - datetime.combine(date.min, arrival)
    return sub                                                                         


