from django.conf import settings
from django.shortcuts import get_object_or_404, render
from products.models import Product, Tag
def home(request):
    """view for index page"""
    products = Product.objects.all()
    tag = get_object_or_404(
        Tag, tag='clearance'
    )
    tagged_products = []
    for product in products:
        for tag_check in product.tags.all():
            if tag == tag_check:
                tagged_products.append(product)
    if len(tagged_products) > 0:
        context = {
            'clearance': tagged_products,
        }
    return render(request, 'home/home.html', context=context)