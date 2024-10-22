from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from checkout.models import Order, OrderLineItem
from dashboard.models import Dashboard
from products.models import Brand, Category, Product, Tag
from django.contrib import messages
from django.db.models.query import QuerySet

from reviews.models import Review

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
        reviews = Review.objects.all()
        review_related_products = []
        categories = Category.objects.all()
        tags = Tag.objects.all()
        brands = Brand.objects.all()
        for review in reviews:
            order_lineitem = OrderLineItem.objects.get(review=review)
            product = Product.objects.get(id=order_lineitem.product.id)
            review_related_products.append(product)
        product_reviews = zip(reviews, review_related_products)
        context = {
            'orders': orders,
            'product_reviews': product_reviews,
            'categories': categories,
            'brands': brands,
            'tags': tags
        }
    else:
        template = 'dashboard/profile.html'
        profile = get_object_or_404(Dashboard, user=request.user.id)
        orders = profile.orders.all()
        lineitems = []
        for order in orders:
            order_lineitems = order.lineitems.all()
            for order_lineitem in order_lineitems:
                review = Review.objects.get(order=order_lineitem)
                if review.rating is None:
                    lineitems.append(order_lineitem)
        context = {
            'orders': orders,
            'profile': profile,
            'lineitems': lineitems
        }
    return render(request, template, context)


@require_POST
def add_tag(request):
    if 'tag' in request.POST and 'friendly_name':
        Tag.objects.create(
            tag=request.POST.get('tag'),
            friendly_name=request.POST.get('friendly_name')
        )
        messages.success(request, 'Tag added successfully')
        return redirect('dashboard')
    else:
        messages.error(request, 'Tag could not be added')
        return redirect('dashboard')


@require_POST
def add_category(request):
    if 'category' in request.POST and 'friendly_name':
        Category.objects.create(
            category=request.POST.get('tag'),
            friendly_name=request.POST.get('friendly_name')
        )
        messages.success(request, 'Tag added successfully')
        return redirect('dashboard')
    else:
        messages.error(request, 'Tag could not be added')
        return redirect('dashboard')


@require_POST
def add_brand(request):
    if 'brand' in request.POST and 'friendly_name':
        Brand.objects.create(
            brand=request.POST.get('brand'),
            support_page=request.POST.get('support_page')
        )
        messages.success(request, 'Tag added successfully')
        return redirect('dashboard')
    else:
        messages.error(request, 'Tag could not be added')
        return redirect('dashboard')