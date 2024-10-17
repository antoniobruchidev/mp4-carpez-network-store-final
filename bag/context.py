from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404

from products.models import Product


def bag(request):

    bag_items = []
    total = 0
    objects = 0

    b = request.session.get('bag', {})

    for product_id in b.keys():
        product = get_object_or_404(Product, pk=product_id)
        total += product.price * b[product_id]
        objects += b[product_id]
        bag_items.append({
            'product_id': product_id,
            'quantity': b[product_id],
            'product': product,
        })

    if total < settings.FREE_DELIVERY_TRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_TRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0
    grand_total = total + delivery

    context = {
        'bag_items': bag_items,
        'total': total,
        'objects': objects,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_treshold': settings.FREE_DELIVERY_TRESHOLD,
        'grand_total': grand_total,
    }
    
    return context