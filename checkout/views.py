from django.conf import settings
from django.shortcuts import render
from bag.context import bag
import stripe
from profiles.forms import AddressForm


# Create your views here.


def checkout(request):
    address_form = AddressForm()
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    
    current_bag = bag(request)
    total = current_bag["grand_total"]
    stripe_total = round(total * 100)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )
    
    context = {
        'form': address_form,
        'client_secret': intent.client_secret,
        'stripe_public_key': stripe_public_key
    }
    return render(request, 'checkout/checkout.html', context)