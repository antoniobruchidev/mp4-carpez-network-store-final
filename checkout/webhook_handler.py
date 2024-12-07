from decimal import Decimal
import json
import socket
import time
from django.http import HttpResponse
from checkout.models import Discount, Order, OrderLineItem
from dashboard.models import Dashboard
from products.models import Product
import stripe
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from email_relay.views import send_confirmation_email


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

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
        discount = intent.metadata.discount
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe_charge = stripe.Charge.retrieve(
             intent.latest_charge
        )
        amount = round(int(intent.amount) / 100, 2)
        if user_id == "ul" or user_id == 'null':
            print(user_id, "user_id check - webhook log")
            profile = None
            user = None
        else:
            user = User.objects.get(id=int(user_id))
            profile = Dashboard.objects.get(user=user)
            print(profile.in_use, ("users profile points in use check - webhook log"))
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
                    order.save()
                    print("order created in place order, webhook log")
                    break
            except Order.DoesNotExist:
                pass
            attempt += 1
            time.sleep(1)
        if order_exists:
            
            send_confirmation_email(order)
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
                            "stripe_pid": pid,
                            "discount": discount
                        },
                        user=profile,
                        status='confirmed'
                    )
                    if discount != "0":
                        d = Discount.objects.get(id=discount)
                        profile.in_use = 0
                        profile.save()
                        order.discount = d
                        order.save()
                        order.update_total()
                        print("order created in webhook and user and discount applied, webhook log")
                    else:
                        profile.points += round(
                            order.grand_total / 100
                        ) * 100
                        profile.save()
                        print("order created in webhook and user applied, no discount applied, webhook log")
                else:
                    order = Order.objects.create(
                        bag_and_shipping_details={
                            "bag": bag,
                            "shipping": shipping,
                            "email": email,
                            "stripe_pid": pid,
                            "discount": discount
                        },
                        status='confirmed'
                    )
                order.save()
                print("order created in webhook and no user and discount applied, webhook log")
                for item_id, quantity in bag.items():
                    p = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=p,
                        quantity=quantity
                    )
                    if p.discount > 0:
                        order_line_item.discounted_price = p.price - Decimal(
                            p.price * p.discount / 100
                        ).__round__(2)
                    order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                    return HttpResponse(content=f'Webhook received: \
                        {event["type"]} | ERROR: {e}', status=500)

        send_confirmation_email(order)
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
