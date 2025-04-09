from django.conf import settings
from checkout.models import Order
from django.template.loader import render_to_string
from custom_adapter import send_email


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
    send_email(subject, body, cust_email)
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
    send_email(subject, body, cust_email)

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
    send_email(subject, body, cust_email)

    return True

