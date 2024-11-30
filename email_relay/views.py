from django.conf import settings
from ecommerce.env import config
from django.template.loader import render_to_string
import requests
# Create your views here.


def send_confirmation_email(order):
    line_items = order.lineitems.all()
    print(line_items)
    """Send the user a confirmation email"""
    cust_email = order.email
    subject = "Order Confirmation"
    body = render_to_string(
        'email_relay/order_confirmation_email.txt',
        {
            'order': order,
            'contact_email': settings.EMAIL_HOST_USER,
            'line_items': line_items
        }
    )
    url = config('EMAIL_RELAY_URL')
    post_data = [
        ('subject', subject),
        ('recipient', cust_email),
        ('body', body),
        ('sender', settings.EMAIL_HOST_USER),
        ('secret', config("FLASK_RELAY_SECRET"))]
        
    result = requests.post(url, data=post_data)

    return True

        

