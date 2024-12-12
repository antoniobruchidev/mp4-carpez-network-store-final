from django.conf import settings
from django.shortcuts import render
from products.models import Product, Tag

def home(request):
    """view for index page"""
    products = Product.objects.all()
    try:
        tag = Tag.objects.get(tag=settings.HOMEPAGE_CAROUSEL_TAG)
    except Tag.DoesNotExist:
        tag = Tag.objects.get(tag="clearance")
    tagged_products = []
    for product in products:
        for tag_check in product.tags.all():
            if tag == tag_check:
                tagged_products.append(product)
    context = {
        "tagged_products": tagged_products,
        "tag": tag.friendly_tag
    }
    return render(request, "home/home.html", context=context)
