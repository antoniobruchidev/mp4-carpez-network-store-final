from django.conf import settings
from django.shortcuts import redirect
from checkout.models import Order
from ecommerce.env import config
from django.template.loader import render_to_string
import requests
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
# Create your views here.


def send_confirmation_email(order):
    """Send the user a confirmation email"""
    line_items = order.lineitems.all()
    discounted_amount = None
    if order.discount:
        discounted_amount = order.grand_total - (
            order.delivery_cost + order.order_total
        )
    cust_email = order.email
    subject = "Carpez Network - Order Confirmation"
    body = render_to_string(
        'email_relay/order_confirmation_email.txt',
        {
            'order': order,
            'contact_email': settings.EMAIL_HOST_USER,
            'line_items': line_items,
            'discount': order.discount,
            'discounted_amount': discounted_amount
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


def send_dispatch_email(order_id):
    """Send the user a notification email"""
    order = Order.objects.get(id=order_id)
    line_items = order.lineitems.all()
    discounted_amount = None
    if order.discount:
        discounted_amount = order.grand_total - (
            order.delivery_cost + order.order_total
        )
    cust_email = order.email
    subject = "Carpez Network - Order Notification - Dispatch"
    body = render_to_string(
        'email_relay/order_dispatched_email.txt',
        {
            'order': order,
            'contact_email': settings.EMAIL_HOST_USER,
            'line_items': line_items,
            'discount': order.discount,
            'discounted_amount': discounted_amount
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


def send_delivered_email(order_id):
    """Send the user a notification email"""
    order = Order.objects.get(id=order_id)
    line_items = order.lineitems.all()
    discounted_amount = None
    if order.discount:
        discounted_amount = order.grand_total - (
            order.delivery_cost + order.order_total
        )

    cust_email = order.email
    subject = "Carpez Network - Order Notification - Delivery"
    body = render_to_string(
        'email_relay/order_delivered_email.txt',
        {
            'order': order,
            'contact_email': settings.EMAIL_HOST_USER,
            'line_items': line_items,
            'discount': order.discount,
            'discounted_amount': discounted_amount
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


def receive_error(request):
    if 'to' in request.GET:
        email = EmailMultiAlternatives(
        "This is a test",
        "This is so much a test",
        settings.EMAIL_HOST_USER,
        [request.GET["to"]]
        )
        email.fail_silently=False
        try:
            email.send()
            messages.success(request, "Email sent")
        except Exception as e:
            print(e)
            messages.error(request, e.__str__())
    return redirect("home")
        

