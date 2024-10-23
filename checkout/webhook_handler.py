import json
import socket
import time
from django.http import HttpResponse
from checkout.models import Order, OrderLineItem
from dashboard.models import Dashboard
from products.models import Product
import stripe
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from email_relay.views import request_email_order_confirmation


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email
        subject = "Carpez Network - Order Confirmation"
        body = render_to_string(
            'checkout/email/confirmation_email.txt',
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
        except socket.gaierror as e:
            print(e)
        except Exception as e:
            print(e)

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        bag = json.loads(intent.metadata.bag)
        email = intent.metadata.email
        shipping = dict(intent.shipping)
        user_id = intent.metadata.user_id
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe_charge = stripe.Charge.retrieve(
             intent.latest_charge
        )
        if user_id == "ul" or user_id == 'null':
            profile = None
            user = None
        else:
            user = User.objects.get(id=int(user_id))
            profile = Dashboard.objects.get(user=user)
        print(user,profile,"1")
        amount = round(int(intent.amount) / 100, 2)
        billing_details = stripe_charge.billing_details
        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    stripe_pid=pid,
                    grand_total=amount
                )
                if order:
                    order_exists = True
                    order.status = 'confirmed'
                    order.billing_details = billing_details
                    if profile:
                        profile.points += round(amount / 100) * 100
                        profile.save()
                        order.user = profile
                        print(order.user,"2")
                    order.save()
                    break
            except Order.DoesNotExist:
                pass
            attempt += 1
            print(attempt,"2")
            time.sleep(1)
        if order_exists:
            
            res = request_email_order_confirmation(order.id)
            print(res,"1")
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: \
                    Verified order already in database',
                status=200)
        else:
            try:
                if user:
                    order = Order.objects.create(
                        bag_and_shipping_details={
                            "bag": bag,
                            "shipping": shipping,
                            "email": email,
                            "stripe_pid": pid
                        },
                        user=profile,
                        status='confirmed'
                    )
                    profile.points += round(amount / 100) * 100
                    profile.save()
                else:
                    order = Order.objects.create(
                        bag_and_shipping_details={
                            "bag": bag,
                            "shipping": shipping,
                            "email": email,
                            "stripe_pid": pid
                        },
                        status='confirmed'
                    )
                order.save()
                for item_id, quantity in bag.items():
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=quantity
                    )
                    order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                    return HttpResponse(content=f'Webhook received: \
                        {event["type"]} | ERROR: {e}', status=500)

        request_email_order_confirmation(order.id)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created\
                order in webhook',
            status=200)

    def handle_payment_intent_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_created(self, event):
        """
        Handle the payment_intent.created webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
