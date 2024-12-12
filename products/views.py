from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from checkout.models import Order, OrderLineItem
from dashboard.models import Dashboard
from products.forms import ProductForm
from products.models import Brand, Category, Product, Tag
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib import messages

from django.contrib.auth.models import User
from reviews.models import Review

# Create your views here.


def get_products(request):
    """View to return all available product
    or all available products associated with a tag,
    or filter available products by an user query"""
    if request.user.is_superuser:
        products = Product.objects.all()
    else:
        products = Product.objects.exclude(available=False)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    category = None
    sort = None
    direction = None
    query = None

    if request.GET:
        if 'category' in request.GET:
            if request.GET['category'] != "":
                category = get_object_or_404(
                    Category, name=request.GET['category']
                )
                products = products.filter(category=category)

        if 'brand' in request.GET:
            if request.GET['brand'] != "":
                brand = get_object_or_404(
                    Brand, brand=request.GET['brand']
                )
                products = products.filter(brand=brand)
            
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
                
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            
            products = products.order_by(sortkey)

            if request.GET['sort'] == 'rating':
                products = products.exclude(rating__isnull=True)

        if 'q' in request.GET:
            query = request.GET['q']    
            queries = (
                Q(name__icontains=query) | Q(
                    description__icontains=query
                    ) | Q(brand__brand__icontains=query)
                )
            products = products.filter(queries).distinct()
        if 'tag' in request.GET:
            if request.GET['tag'] != "":
                tag = get_object_or_404(
                    Tag, tag=request.GET['tag']
                )
                tagged_products = []
                for product in products:
                    for tag_check in product.tags.all():
                        if tag == tag_check:
                            tagged_products.append(
                                product)
                products = tagged_products
                            
    discounted_prices = []
    for product in products:
        if product.discount > 0:
            discounted_price = product.price - Decimal(
                product.price * product.discount / 100
            ).__round__(2)
        else:
            discounted_price = None
        discounted_prices.append(discounted_price)
    products_and_discounts = zip(products, discounted_prices)
    current_sorting = f'{sort}_{direction}'
    
    context = {
        'products': products_and_discounts,
        'search-term': query,
        'category': category,
        'categories': categories,
        'current_sorting': current_sorting,
        'tags': tags,
    }
    return render(request, 'products/products.html', context)


def get_product_details(request, product_id):
    """View to return the details of a given product"""
    product = get_object_or_404(Product, id=product_id)
    order_lineitems = OrderLineItem.objects.filter(product=product_id)
    usernames = []
    reviews = []
    product_badges = []
    tags = Tag.objects.all()
    for tag in tags:
        if tag in product.tags.all():
            product_badges.append(tag)
    for lineitem in order_lineitems:
        review = Review.objects.get(order=lineitem)
        if review.rating != None:
            order = Order.objects.get(id=lineitem.order.id)
            if order.user != None:
                user = User.objects.get(id=order.user.id)
                usernames.append(user.username)
                reviews.append(review)
    product_reviews = zip(reviews, usernames)
    if product.discount > 0:
        discounted_price = product.price - Decimal(
            product.price * product.discount / 100
        ).__round__(2)
    else:
        discounted_price = None
    template = 'products/product_details.html'
    context = {
        'product': product,
        'product_reviews': product_reviews,
        'tags': product_badges,
        'brand': product.brand,
        'category': product.category,
        'discounted_price': discounted_price
    }
    return render(request, template, context)


@login_required
def add_product(request):
    """View to add a product to the store"""
    if request.user.is_superuser:
        form = ProductForm()
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save()
                messages.success(request, "Successfully added product")
                return redirect(
                    reverse('get_product_details', args=[product.id])
                )
            else:
                messages.error(
                    request,
                    "Form is not valid, please double check the data."
                )

        template = 'products/add_product.html'
        context = {
            'form': form,
        }
        return render(request, template, context)
    else:
        messages.error(request, "You are not allowed to add products")
        return redirect(reverse('home'))


@login_required
def edit_product_details(request, product_id):
    """View to edit a product in the store"""
    if request.user.is_superuser:
        product = get_object_or_404(Product, id=product_id)
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, "Successfully updated product")
                return redirect(
                    reverse('get_product_details', args=[product.id])
                    )
            else:
                messages.error(
                    request, "Failed to update, ensure the data is valid"
                    )
        else:
            form = ProductForm(instance=product)
            messages.info(request, f"You are editing {product.name}")
        template = 'products/edit_product.html'
        context = {
            'form': form,
            'product': product,
        }

        return render(request, template, context)
    else:
        messages.error(request, "Authorization denied, you are not an admin.")
        return redirect(reverse('home'))


@login_required
def delete_product(request, product_id):
    """Delete a product from the store"""
    if request.user.is_superuser:
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        messages.success(request, "Product deleted.")
        return redirect(reverse('get_products'))
    else:
        messages.error(request, "Authorization denied, you are not an admin.")
        return redirect(reverse('home'))
