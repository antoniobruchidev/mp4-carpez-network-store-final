from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_POST

from checkout.models import Discount, Order, OrderLineItem
from dashboard.models import Dashboard
from products.models import Brand, Category, Product, Tag
from django.contrib import messages

from reviews.models import Review
from email_relay.views import (
    send_dispatch_email,
    send_delivered_email,
    send_confirmation_email
)

# Create your views here.

@login_required
def dashboard(request):
    if request.user.is_superuser:
        template = 'dashboard/product_management.html'
        if request.GET:
            if 'sku' in request.GET:
                sku = request.GET['sku'] 
                try:
                    product = Product.objects.get(sku=sku)
                except Product.DoesNotExist:
                    try:
                        order = Order.objects.get(order_number=sku)
                        return redirect('checkout_success', order.order_number)
                    except Order.DoesNotExist:
                        messages.error(
                            request,
                            f"We couldn't find  {sku} either as SKU or as \
                            Order Number in the database")
                    return redirect(reverse('dashboard'))
                        
                return redirect('get_product_details', product.id)
        orders = Order.objects.all().order_by('-date').values()
        reviews = Review.objects.all()
        review_related_products = []
        categories = Category.objects.all()
        tags = Tag.objects.all()
        brands = Brand.objects.all()
        discounts = Discount.objects.all()
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
            'tags': tags,
            'discounts': discounts
        }
    else:
        template = 'dashboard/profile.html'
        profile = get_object_or_404(Dashboard, user=request.user.id)
        orders = Order.objects.filter(user=profile).order_by('-date')
        lineitems = []
        for order in orders:
            print(order)
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
    if request.user.is_superuser:
        if 'tag' in request.POST and 'friendly_tag' in request.POST:
            Tag.objects.create(
                tag=request.POST.get('tag'),
                friendly_tag=request.POST.get('friendly_tag')
            )
            messages.success(request, 'Tag added successfully')
            return redirect('dashboard')
        else:
            messages.error(request, 'Tag could not be added')
            return redirect('dashboard')


@require_POST
def add_category(request):
    if request.user.is_superuser:
        if 'category' in request.POST and 'friendly_name' in request.POST:
            Category.objects.create(
                category=request.POST.get('tag'),
                friendly_name=request.POST.get('friendly_name')
            )
            messages.success(request, 'Tag added successfully')
            return redirect('dashboard')
        else:
            messages.error(request, 'Tag could not be added')
            return redirect('dashboard')
    else:
        messages.error(request, "Permission denied")
        return redirect('home')


@require_POST
def add_brand(request):
    if request.user.is_superuser:
        if 'brand' in request.POST and 'support_page' in request.POST:
            Brand.objects.create(
                brand=request.POST.get('brand'),
                support_page=request.POST.get('support_page')
            )
            messages.success(request, 'Tag added successfully')
            return redirect('dashboard')
        else:
            messages.error(request, 'Tag could not be added')
            return redirect('dashboard')
    else:
        messages.error(request, "Permission denied")
        return redirect('home')


@require_POST
def edit_order(request, order_id):
    if request.user.is_superuser:
        if 'status' in request.POST:
            order = Order.objects.get(id=order_id)
            order.status = request.POST.get('status')
            order.save()
            if order.status == "confirmed":
                send_confirmation_email(order.id)
            if order.status == "dispatched":
                send_dispatch_email(order.id)
            elif order.status == "delivered":
                send_delivered_email(order.id)
            print(order.status)
            messages.success(request, 'Order status updated successfully and sent notification email')
            return redirect('dashboard')
        else:
            messages.error(request, 'Order status could not be updated')
            return redirect('dashboard')
    else:
        messages.error(request, "Permission denied")
        return redirect('home')


@require_POST
def add_discount(request):
    if request.user.is_superuser:
        if 'discount' in request.POST and 'points' in request.POST:
            Discount.objects.create(
                points=request.POST.get('points'),
                discount=request.POST.get('discount')
            )
            messages.success(request, 'Discount added successfully')
            return redirect('dashboard')
        else:
            messages.error(request, 'Discount could not be added')
            return redirect('dashboard')
    else:
        messages.error(request, "Permission denied")
        return redirect('home')
    

@require_POST
def delete_tag(request, tag_id):
    if request.user.is_superuser:
        try:
            tag = Tag.objects.get(id=tag_id)
            if tag.tag == 'desktop' or tag.tag == 'laptop':
                messages.error(request, 'Desktop and Laptop tags are required. Aborted.')
                return HttpResponse(status=200)
            else:
                tag.delete()
                messages.success(request, 'Tag deleted successfully')
                return HttpResponse(status=200)
        except Exception as e:
            messages.error(
            request,
            "Sorry we could not accomodate your request at\
            this time. Please trye again later.",
        )
        return HttpResponse(content=e, status=400)
    else:
        messages.error(request, "Permission denied")
        return redirect('home')


@require_POST
def delete_discount(request, discount_id):
    if request.user.is_superuser:
        discount = Discount.objects.get(id=discount_id)
        discount.delete()
        messages.success(request, 'Discount deleted successfully')
        return redirect('dashboard')
    else:
        messages.error(request, "Permission denied")
        return redirect('home')


@require_POST
def delete_brand(request, brand_id):
    if request.user.is_superuser:
        brand = brand.objects.get(id=brand_id)
        brand.delete()
        messages.success(request, 'Brand deleted successfully')
        return redirect('dashboard')
    else:
        messages.error(request, "Permission denied")
        return redirect('home')


@require_POST
def delete_category(request, category_id):
    if request.user.is_superuser:
        category = Category.objects.get(id=category_id)
        category.delete()
        messages.success(request, 'Category deleted successfully')
        return redirect('dashboard')
    else:
        messages.error(request, "Permission denied")
        return redirect('home')