from django import forms

from checkout.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('bag_and_shipping_details',)

