from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from dashboard.models import Dashboard
from products.models import Product
from django.contrib import messages

from checkout.models import Discount


def view_bag(request):
    """ A view to return the bag contents page """
    profile = None
    discounts = None
    discounts_available = None
    if str(request.user) != "AnonymousUser":
        profile = Dashboard.objects.get(user=request.user)
        discounts = Discount.objects.exclude(available=False)
        discounts_available = False
        for discount in discounts:
            if profile.points >= discount.points:
                discounts_available = True
    template = 'bag/bag.html'
    context = {
        'on_bag_page': True,
        'profile': profile,
        'discounts': discounts,
        'discounts_available': discounts_available
    }
    return render(request, template, context)


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


def update_item_quantity(request, product_id):
    """ Update quantity of item in bag """
    bag = request.session.get('bag', {})
    new_quantity = int(request.POST.get('quantity'))
    if new_quantity > 0:
        bag[product_id] = new_quantity
        if new_quantity > 99:
            bag[product_id] = 99
            request.session['bag'] = bag
            messages.warning(request, "Successfully updated quantity, but maximum is 99")
            return HttpResponse(status=200)
        request.session['bag'] = bag
        messages.success(request, "Successfully updated quantity")
        return HttpResponse(status=200)
    elif new_quantity == 0:
        del bag[product_id]
        request.session['bag'] = bag
        messages.success(request, "Successfully updated quantity")
        return HttpResponse(status=200)
    else:
        messages.error(request, "Quantity cannot be less than 0")
        return HttpResponse(status=200)



def remove_from_bag(request, product_id):
    """ Remove item from bag """
    bag = request.session.get('bag', {})
    if bag[product_id]:
        del bag[product_id]
    request.session['bag'] = bag
    messages.success(request, "Successfully removed item")
    return redirect('view_bag')
