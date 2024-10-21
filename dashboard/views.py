from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from checkout.models import Order
from dashboard.models import Dashboard
from products.models import Product
from django.contrib import messages

# Create your views here.

@login_required
def dashboard(request):
    if request.user.is_superuser:
        template = 'dashboard/product_management.html'
        if request.GET:
            print(request.GET)
            if 'sku' in request.GET:
                sku = request.GET['sku'] 
                try:
                    product = Product.objects.get(sku=sku)
                except Product.DoesNotExist:
                    messages.error(
                        request,
                        "The SKU {sku} was not found in the database")
                return redirect('get_product_details', product.id)
        orders = Order.objects.all()
        context = {
            'orders': orders,
        }
    else:
        template = 'dashboard/profile.html'
        profile = get_object_or_404(Dashboard, user=request.user.id)
        orders = profile.orders.all()
        context = {
            'orders': orders,
            'profile': profile,
        }
    return render(request, template, context)