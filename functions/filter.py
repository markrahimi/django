from django.contrib.humanize.templatetags.humanize import intcomma
from utils.time_date_calculations import calculate_date_difference
from django.utils import timezone
from datetime import datetime
from django import template
import jdatetime

register = template.Library()


def calculate_date_difference(start_date, end_date):
    date_format = "%Y-%m-%d"
    start = datetime.strptime(str(start_date), date_format)
    end = datetime.strptime(str(end_date), date_format)
    delta = end - start
    return delta.days
    

def calculate_time_difference(start_datetime, end_datetime):
    start_datetime = timezone.localtime(start_datetime)
    end_datetime = timezone.localtime(end_datetime)
    date_format = "%Y-%m-%d %H:%M:%S.%f%z"
    start = datetime.strptime(str(start_datetime), date_format)
    end = datetime.strptime(str(end_datetime), date_format)
    delta = end - start
    return delta.seconds


# -------------------------------------------------------------------------------------------------------------------------------------

@register.filter(name='currency')
def currency(value):
    return '{:,}'.format(int(value))


@register.filter(name='gregorian_date_to_jalali')
def gregorian_date_to_jalali(value):
    date_format = "%Y-%m-%d"
    thisdate = datetime.strptime(str(value), date_format)
    return jdatetime.date.fromgregorian(day = thisdate.day, month = thisdate.month, year = thisdate.year).strftime("%Y/%m/%d")


@register.filter(name='gregorian_datetime_to_jalali')
def gregorian_datetime_to_jalali(value):
    date_format = "%Y-%m-%d"
    thisdate = datetime.strptime(str(value.date()), date_format)
    return jdatetime.date.fromgregorian(day = thisdate.day, month = thisdate.month, year = thisdate.year).strftime("%Y/%m/%d")


@register.simple_tag
@register.filter(name='calculate_discount_percentage')
def calculate_discount_percentage(price, offer_price):
    try:
        price = int(price)
        offer_price = int(offer_price)
        
        return round(((price - offer_price) / price) * 100)
    except:
        return 'خطا'



@register.filter(name='payment_status_to_fa')
def payment_status_to_fa(value):
    payment_status = {
        '0':'منتظر پرداخت',
        '1':'منتظر تایید رسید',
        '2':'پرداخت شده',
    }
    return payment_status[value]


@register.filter(name='payment_method_to_fa')
def payment_method_to_fa(value):
    payment_method = {
        '0':'پرداخت نشده',
        '1':'پرداخت با فیش واریز',
        '2':'پرداخت اینترنتی',
        '3':'پرداخت حضوری با دستگاه',
        '4':'پرداخت حضوری نقد',
    }
    return payment_method[value]



@register.filter(name='sex_to_fa')
def sex_to_fa(value):
    sex = {
        'male': 'مرد',
        'female': 'زن'
    }
    return sex[value]


@register.filter(name='calculate_age')
def calculate_age(value):
    today = datetime.now().date()
    delta = calculate_date_difference(value, today)
    return int(delta / 365)



