from django import template
from datetime import datetime, date


register = template.Library()

# this filter is for getting total passenger by addding number of adult and child
@register.filter(name="passengers")
def passengers(adult, child):
    adult = int(adult)
    child = int(child)
    return adult + child

# this filter is for multiplying total passenger with class price
@register.filter(name="multiply")
def multiply(price, passenger):
    return passenger * price

# this filter is for getting duration between departure time to arrival time
@register.filter(name="duration")
def duration(departure, arrival):
    sub = datetime.combine(date.min, departure) - datetime.combine(date.min, arrival)
    return sub  
                                                                      