from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product
from django.contrib import messages


def view_bag(request):
    """ A view to return the bag contents page """
    template = 'bag/bag.html'
    return render(request, template)


def add_to_bag(request, product_id):
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})
    product = get_object_or_404(Product, pk=product_id)

    if product_id in list(bag.keys()):
        bag[product_id] += 1
    else:
        bag[product_id] = 1

    request.session['bag'] = bag
    messages.success(request, f"Successfully added {product.name}")
    return redirect(redirect_url)