import json
import socket
import time
from django.http import HttpResponse
from checkout.models import Order, OrderLineItem
from products.models import Product
import stripe
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


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
        print(pid)
        bag = json.loads(intent.metadata.bag)
        email = intent.metadata.email
        shipping = dict(intent.shipping)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )
        amount = round(stripe_charge.amount / 100, 2)
        billing_details = stripe_charge.billing_details
        order_exists = False
        attempt = 1
        while attempt <= 5:
            print(attempt, pid, amount)
            try:
                order = Order.objects.get(
                    stripe_pid=pid,
                    grand_total=amount
                    )
                order.billing_details = billing_details
                print(order, order_exists)
                if order:
                    order_exists = True
                    break
            except Order.DoesNotExist:
                pass
            
            attempt += 1
            time.sleep(1)
        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: \
                        Verified order already in database',
                    status=200)
        else:
            try:
                order = Order.objects.create(
                    bag_and_shipping_details={
                        "bag": bag,
                        "shipping": shipping,
                        "email": email,
                        "stripe_pid": pid
                    }
                )
                order.save(pid)
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

        self._send_confirmation_email(order)
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