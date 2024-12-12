from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_POST

from checkout.models import Discount, Order, OrderLineItem
from dashboard.models import Dashboard
from products.models import Brand, Category, Product, Tag
from django.contrib import messages
from django.core.paginator import Paginator

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
                        return redirect(
                            'checkout_success', order.order_number
                        )
                    except Order.DoesNotExist:
                        messages.error(
                            request,
                            f"We couldn't find  {sku} either as SKU or as \
                            Order Number in the database")
                    return redirect(reverse('dashboard'))
                        
                return redirect('get_product_details', product.id)
        orders = Order.objects.all().order_by('-date')
        paginated_orders = Paginator(orders, 20)
        if 'page' in request.GET:
            page = int(request.GET.get("page"))
        else:
            page = 1
        page_orders = paginated_orders.get_page(page)
        page_display = "{} to {} of {} entries".format(
            int(page - 1) * 20 + 1,
            int(page) * 20,
            paginated_orders.count
        )
        if page == paginated_orders.num_pages:
            page_display = "{} to {} of {} entries".format(
                int(page - 1) * 20 + 1,
                paginated_orders.count,
                paginated_orders.count
            )
        page_count = []
        for item in range(0,paginated_orders.num_pages):
            page_count.append(item + 1)
        reviews = Review.objects.exclude(rating=None).filter(
            store_answer=None
        )
        review_related_products = []
        review_customer_emails = []
        categories = Category.objects.all()
        tags = Tag.objects.all()
        brands = Brand.objects.all()
        discounts = Discount.objects.all()
        for review in reviews:
            product = Product.objects.get(id=review.order.product.id)
            order = Order.objects.get(id=review.order.order.id)
            review_related_products.append(product)
            review_customer_emails.append(order.email)
        product_reviews = zip(
            reviews, review_related_products, review_customer_emails
        )
        context = {
            'orders': page_orders,
            'product_reviews': product_reviews,
            'categories': categories,
            'brands': brands,
            'tags': tags,
            'discounts': discounts,
            'paginator': { 
                'pages': paginated_orders.num_pages,
                'current_page': page,
                'previous_page':page - 1,
                'next_page': page + 1,
                'entries': paginated_orders.count,
                'page_display': page_display,
                'page_count': page_count
            }
        }
    else:
        template = 'dashboard/profile.html'
        profile = get_object_or_404(Dashboard, user=request.user.id)
        orders = Order.objects.filter(user=profile).order_by('-date')
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
            'lineitems': lineitems,
            'on_profile_page': True
        }
    return render(request, template, context)


@require_POST
def add_tag(request):
    if request.user.is_superuser:
        data = dict()
        if 'tag' in request.POST and 'friendly_tag' in request.POST:
            try:
                tag = Tag.objects.create(
                    tag=request.POST.get('tag'),
                    friendly_tag=request.POST.get('friendly_tag')
                )
                data["success"] = 'Tag added successfully'
                data["new_tag_id"] = tag.id
                data["new_tag_name"] = tag.friendly_tag
                status = 200
            except Exception as error:
                status = 500
                if 'unique constraint' in error.__str__():
                    data["error"] = "Attempt to add tag violates unique \
                        fields rule, double check if you already have \
                        the desired tag."
                else:
                    data["error"] = error.__str__
            return JsonResponse(data=data, status=status)
        else:
            data["error"] = 'Tag could not be added, invalid input'
            return JsonResponse(data=data, status=422)
    else:
        data["error"] = "Permission denied"
        return JsonResponse(data=data, status=403)


@require_POST
def add_category(request):
    if request.user.is_superuser:
        data = dict()
        if 'name' in request.POST and 'friendly_name' in request.POST:
            try:
                category = Category.objects.create(
                    name=request.POST.get('name'),
                    friendly_name=request.POST.get('friendly_name')
                )
                data["success"] = 'Category added successfully'
                data["new_category_id"] = category.id
                data["new_category_name"] = category.friendly_name
                status=200
            except Exception as error:
                status = 500
                if 'unique constraint' in error.__str__():
                    data["error"] = "Attempt to add category violates \
                        unique fields rule, double check if you already \
                        have the desired category."
                else:
                    data["error"] = error.__str__()
            return JsonResponse(data=data, status=status)
        else:
            data["error"] = 'Category could not be added, invalid input'
            return JsonResponse(data=data, status=422)
    else:
        data["error"] = "Permission denied"
        return JsonResponse(data=data, status=403)


@require_POST
def add_brand(request):
    if request.user.is_superuser:
        data = dict()
        if 'brand' in request.POST and 'support_page' in request.POST:
            try:
                brand = Brand.objects.create(
                    brand=request.POST.get('brand'),
                    support_page=request.POST.get('support_page')
                )
                data["success"] = 'Brand added successfully'
                data["new_brand_id"] = brand.id
                data["new_brand_name"] = brand.brand
                status = 200
            except Exception as error:
                status = 500
                if 'unique constraint' in error.__str__():
                    data["error"] = "Attempt to add brand violates unique \
                        field rule, double check if you already have \
                        the desired brand."
                else:
                    data["error"] = error.__str__()
            return JsonResponse(data=data, status=status)
        else:
            data["error"] = 'Brand could not be added, invalid input'
            return JsonResponse(data=data, status=422)
    else:
        data["error"] = "Permission denied"
        return JsonResponse(data=data, status=403)


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
            messages.success(request, 'Order status updated successfully \
                             and sent notification email')
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
        data = dict()
        if 'discount' in request.POST and 'points' in request.POST:
            try:
                discount = Discount.objects.create(
                    points=request.POST.get('points'),
                    discount=request.POST.get('discount'),
                    max_discount=request.POST.get('max_discount')
                )
                data["success"] = 'Discount added successfully'
                data["new_discount_id"] = discount.id
                data["new_discount"] = discount.__str__()
                data["new_discount_percentage"] = discount.discount
                status = 200
            except Exception as error:
                status = 500
                data["error"] = error.__str__()
            return JsonResponse(data=data, status=status)
        else:
            data["error"] = 'Discount could not be added, invalid inputs'
            return JsonResponse(data=data, status=422)
    else:
        data["error"] = "Permission denied"
        return JsonResponse(data=data, status=403)


@require_POST
def delete_tag(request, tag_id):
    if request.user.is_superuser:
        data = dict()
        try:
            tag = Tag.objects.get(id=tag_id)
            if (tag.tag == 'desktop' or tag.tag == 'laptop' or
                tag.tag == 'clearance'):
                data['error'] = 'Desktop, Laptop and Clearance tags are \
                     required. Aborted.'
                status = 403
            else:
                tag.delete()
                data['success'] = 'Tag deleted successfully.'
                status=200
        except Exception as e:
            data["error"] = e.__str__()
            status = 500
        except Tag.DoesNotExist:
            data["error"] = "Tag to be deleted does not exist."
            status = 404
        return JsonResponse(data=data, status=status)
    else:
        return JsonResponse(status=403)


@require_POST
def delete_discount(request, discount_id):
    if request.user.is_superuser:
        data = dict()
        try:
            discount = Discount.objects.get(id=discount_id)
            discount.delete()
            data['success'] = 'Discount deleted successfully.'
            status=200
        except Exception as e:
            data["error"] = e.__str__()
            status = 500
        except Discount.DoesNotExist:
            data["error"] = "Discount to be deleted does not exist."
            status = 404
        return JsonResponse(data=data, status=status)
    else:
        return JsonResponse(status=403)


@require_POST
def delete_brand(request, brand_id):
    if request.user.is_superuser:
        data = dict()
        try:
            brand = Brand.objects.get(id=brand_id)
            brand.delete()
            data['success'] = 'Brand deleted successfully.'
            status=200
        except Exception as e:
            data["error"] = e.__str__()
            status = 500
        except Brand.DoesNotExist:
            data["error"] = "Brand to be deleted does not exist."
            status = 404
        return JsonResponse(data=data, status=status)
    else:
        return JsonResponse(status=403)


@require_POST
def delete_category(request, category_id):
    if request.user.is_superuser:
        data = dict()
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
            data['success'] = 'Category deleted successfully.'
            status=200
        except Exception as e:
            data["error"] = e.__str__()
            status = 500
        except Category.DoesNotExist:
            data["error"] = "Category to be deleted does not exist."
            status = 404
        return JsonResponse(data=data, status=status)
    else:
        return JsonResponse(status=403)