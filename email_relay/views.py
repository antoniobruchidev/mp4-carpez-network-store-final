import socket
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from checkout.models import Order
from dashboard.models import Dashboard
from ecommerce.env import config
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
import requests
# Create your views here.


def reset_password(request):
    email = request.GET['email']
    res = request_email_lost_password(email)
    if res:
        return render(request, '/allauth/account/password_reset_done.html')
    
    
def send_confirmation_email(request):
    """Send the user a confirmation email"""
    if request.GET:
        if 'order_id' in request.GET:
            print(request.GET)
            print('user_id' in request.GET)
            order = get_object_or_404(Order, id=int(request.GET['order_id']))
            cust_email = order.email
            subject = "Carpez Network - Order Confirmation"
            body = render_to_string(
                'email_relay/order_confirmation_email.txt',
                {'order': order, 'contact_email': settings.EMAIL_HOST_USER}
            )
            email = EmailMultiAlternatives(
                subject,
                body,
                settings.EMAIL_HOST_USER,
                [cust_email]
            )
            email.fail_silently = False
            try:
                email.send()
                return JsonResponse({'email': 'sent'})
            except socket.gaierror as e:
                print(e)
            except Exception as e:
                print(e)
        if 'user_id' in request.GET:
            user = get_object_or_404(User, id=int(request.GET['user_id']))
            cust_email = user.email
            activation_url = request.GET['activation_url']
            subject = "Carpez Network - Signup Confirmation"
            body = render_to_string(
                'email_relay/signup_confirmation_email.txt',
                {'user': user,
                 'contact_email': settings.EMAIL_HOST_USER,
                 'activation_url': activation_url}
            )
            email = EmailMultiAlternatives(
                subject,
                body,
                settings.EMAIL_HOST_USER,
                [cust_email]
            )
            email.fail_silently = False
            try:
                email.send()
                return JsonResponse({'email': 'sent'})
            except socket.gaierror as e:
                print(e)
            except Exception as e:
                print(e)
        if 'email' in request.GET:
            print("something1")
            user = get_object_or_404(User, email=request.GET['email'])
            print(user)
            cust_email = user.email
            subject = "Carpez Network - Lost Password"
            body = render_to_string(
                'email_relay/lost_password_email.txt',
                {'user': user, 'contact_email': settings.EMAIL_HOST_USER}
            )
            email = EmailMultiAlternatives(
                subject,
                body,
                settings.EMAIL_HOST_USER,
                [cust_email]
            )
            email.fail_silently = False
            try:
                email.send()
                return JsonResponse({'email': 'sent'})
            except socket.gaierror as e:
                print(e)
            except Exception as e:
                print(e)


def request_email_order_confirmation(order_id):
    domain = config('EMAIL_RELAY_DOMAIN')
    req = requests.get(f"{domain}?order_id={order_id}")
    response = req.json()
    if response['email'] == 'sent':
        return True


def request_email_signup(user_id):
    domain = config('EMAIL_RELAY_DOMAIN')
    dashboard = Dashboard.objects.get(user=user_id)
    req = requests.get(f"{domain}?&user_id={user_id}&activation_url={dashboard.activation_url}")
    response = req.json()
    if response['email'] == 'sent':
        print("sent")
        return True


def request_email_lost_password(email):
    domain = config('EMAIL_RELAY_DOMAIN')
    user = get_object_or_404(User, email=email)
    dashboard = Dashboard.objects.get(user=user)
    dashboard.generate_activation_url()
    dashboard.activated = False
    req = requests.get(f"{domain}?email={email}")
    response = req.json()
    if response['email'] == 'sent':
        print("sent")
        return True

