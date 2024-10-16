from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from products.forms import ProductForm
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


def get_products(request):
    """View to return all products"""
    products = Product.objects.all()
    template = 'products/products.html'
    context = {
        'products': products
    }
    return render(request, template, context)


def get_product_details(request, product_id):
    """View to return the details of a given product"""
    product = get_object_or_404(Product, id=product_id)
    template = 'products/product_details.html'
    context = {
        'product': product
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
                print(product.id)
                messages.success(request, "Successfully added product")
                return redirect(reverse('get_product_details', args=[product.id]))
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
