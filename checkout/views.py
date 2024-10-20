import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from bag.context import bag
import stripe

from django.urls import reverse
from django.contrib import messages

from checkout.forms import OrderForm
from checkout.models import Order, OrderLineItem
from products.models import Product


# Create your views here.


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get("client_secret").split("_secret")[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(
            pid,
            metadata={
                "bag": json.dumps(request.session.get("bag", {})),
                "username": str(request.user),
                "email": request.POST.get("email"),
                "shipping": request.POST.get("shipping"),
                "billing": request.POST.get("billing")
            },
        )
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(
            request,
            "Sorry we could not accomodate your request at\
            this time. Please trye again later.",
        )
        return HttpResponse(content=e, status=400)


def place_order(request):
    body = request.body.decode('utf-8')
    json_body = json.loads(body)
    b = json.loads(json.loads(json_body['bag']))
    e = json_body['email']
    s = json.loads(json_body['shipping'])
    print(b, type(b))
    pid = json_body['stripe_pid'].replace('"','')
    bag_and_shipping_details = {
        'bag': b,
        'stripe_pid': pid,
        'shipping': s,
        'email': e
    }
    order_form = OrderForm({
        'bag_and_shipping_details': bag_and_shipping_details,
    })
    try:
        order = Order.objects.get(stripe_pid=pid)
        order_exist = True
    except Order.DoesNotExist:
        order_exist = False
        
    if order_form.is_valid() and not order_exist:
        order = order_form.save()
        for item_id, quantity in b.items():
            try:
                product = Product.objects.get(id=item_id)
                order_line_item = OrderLineItem(
                    order=order, product=product, quantity=quantity
                )
                order_line_item.save()
                
            except Product.DoesNotExist:
                messages.error(
                    request,
                    (
                        "One of the products in your bag wasn't found \
                        in our database."
                        "Please call us for assistance!"
                    ),
                )
                order.delete()
                return redirect(reverse("view_bag"))
    
        return JsonResponse({'message': order.order_number})
    else:
        return JsonResponse({'message': 'form not valid'})


def checkout(request):
    if request.method == 'POST':
        print(request.POST)
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
        'client_secret': intent.client_secret,
        'stripe_public_key': stripe_public_key
    }
    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
       
    messages.success(
        request,
        f"Order successfully processed! \
        Your order number is {order_number}, a confirmation \
        email will be sent to {order.bag_and_shipping_details['email']}.",
    )

    if "bag" in request.session:
        del request.session["bag"]

    template = "checkout/checkout_success.html"
    context = {
        "order": order,
    }

    return render(request, template, context)