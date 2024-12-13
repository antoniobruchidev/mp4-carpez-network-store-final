import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
import json

from dashboard.models import Dashboard
from products.models import Product

# Create your models here.


class Discount(models.Model):
    points = models.IntegerField(null=False, blank=False)
    discount = models.IntegerField(null=False)
    max_discount = models.IntegerField(null=False, blank=False)
    available = models.BooleanField(null=False, default=True)

    def __str__(self):
        return f"{self.points} points for {self.discount}% discount."


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        default=0
    )
    order_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0
    )
    discount = models.ForeignKey(
        Discount,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    grand_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0
    )
    bag_and_shipping_details = models.JSONField(
        encoder=DjangoJSONEncoder,
        decoder=json.JSONDecoder
    )
    full_name = models.CharField(max_length=254, null=True, editable=False)
    email = models.EmailField(max_length=254, null=True, editable=False)
    shipping = models.CharField(max_length=254, null=True, editable=False)
    billing_details = models.JSONField(null=True, blank=True)
    stripe_pid = models.CharField(
        max_length=32,
        null=False,
        blank=False,
        editable=False,
        default="before migration"
    )
    user = models.ForeignKey(
        Dashboard,
        null=True,
        blank=True,
        related_name="orders",
        on_delete=models.SET_NULL
    )
    status = models.CharField(
        max_length=10,
        null=False,
        default='pending',
        choices=[
            ('pending', "Pending"),
            ('confirmed', "Confirmed"),
            ('dispatched', "Dispatched"),
            ('delivered', "delivered")
        ]
    )
    
    def _generate_order_number(self):
        """Generate a random unique order number"""
        return uuid.uuid4().hex.upper()
    
    def _generate_order_details(self):
        """Generate content for full name, email, shipping and pid fields"""
        details = self.bag_and_shipping_details
        self.full_name = details['shipping']['name']
        self.email = details['email']
        shipping = details['shipping']['address']['line1']
        if details['shipping']['address']['line2'] is not None:
            shipping_line_2 = details['shipping']['address']['line2']
        else:
            shipping_line_2 = ""
        shipping_locality = details['shipping']['address']['city']
        shipping_postcode = details['shipping']['address']['postal_code']
        shipping_county = details['shipping']['address']['state']
        shipping_country = details['shipping']['address']['country']
        shipping = shipping + " " + shipping_line_2 + " - "
        shipping = shipping + shipping_postcode + " - " + shipping_locality
        shipping = shipping + " - (" + shipping_county + " - " + shipping_country + ")"
        self.shipping = shipping
        self.stripe_pid = details['stripe_pid']

    def save(self, *args, **kwargs):
        """
        Ovverride the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
            self._generate_order_details(*args)
        super().save(*args, **kwargs)

    def update_total(self):
        """update grand total going trought every lineitems and apply
        delivery cost if any.
        """
        self.order_total = (
            self.lineitems.aggregate(
                Sum('lineitem_total'))['lineitem_total__sum'] or 0
        )
        if self.order_total < settings.FREE_DELIVERY_TRESHOLD:
            self.delivery_cost = (
                self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
            )
        else:
            self.delivery_cost = 0
        if self.discount:
            discount = self.order_total * self.discount.discount / 100
            if discount > self.discount.max_discount:
                discount = self.discount.max_discount
            self.grand_total = self.order_total + self.delivery_cost - discount
        else:
            self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='lineitems'
        )
    product = models.ForeignKey(
        Product,
        null=False,
        blank=False,
        on_delete=models.CASCADE
        )
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=False,
        blank=False,
        editable=False
        )
    discounted_price = models.DecimalField(
        null=True,
        blank=True,
        max_digits=6,
        decimal_places=2
        )

    def save(self, *args, **kwargs):
        """Override the save method to set the lineitem total before saving"""
        if self.discounted_price:
            self.lineitem_total = self.discounted_price * self.quantity
        else:
            self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
