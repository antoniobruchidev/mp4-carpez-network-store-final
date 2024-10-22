from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST

from checkout.models import OrderLineItem
from products.models import Product
from reviews.forms import ReviewForm
from reviews.models import Review
from django.contrib import messages
# Create your views here.


@require_http_methods(['GET', 'POST'])
def add_review(request):
    if request.GET:
        if 'lineitem' in request.GET:
            print(request.GET['lineitem'])
            order_lineitem_id = int(request.GET['lineitem'])
            lineitem = get_object_or_404(OrderLineItem, id=order_lineitem_id)
            review = Review.objects.get(order=lineitem)
            form = ReviewForm(instance=review)
            template = 'reviews/add_review.html'
            context = {
                'lineitem': lineitem,
                'form': form
            }
            print(form)
            return render(request, template, context)
        else:
            messages.error(request, "It was not specisified a product to review")
            return redirect('dashboard')
    else:
        order_lineitem_id = int(request.POST.get('lineitem'))
        lineitem = get_object_or_404(OrderLineItem, id=order_lineitem_id)
        review = Review.objects.get(order=lineitem)
        review.title = request.POST.get('title')
        review.content = request.POST.get('content')
        review.rating = request.POST.get('rating')
        review.save()
        reviews = Review.objects.all()
        reviews_count = 0
        reviews_total = 0
        for review in reviews:
            order_lineitem = OrderLineItem.objects.get(review=review)
            print(order_lineitem.product.id, review.rating)
            if order_lineitem.product.id == lineitem.product.id:
                if review.rating is not None:
                    reviews_count += 1
                    reviews_total += review.rating
        rating = round(reviews_total / reviews_count, 1)
        product = get_object_or_404(Product, id=lineitem.product.id)
        product.rating = rating
        product.save()
        
        messages.success(request, f"You successfully reviewed product \
            {lineitem.product.name} ")
        return redirect('dashboard')


@require_POST
def answer_review(request, review_id):
    print(request.user.is_superuser)
    if request.user.is_superuser:
        review = Review.objects.get(id=review_id)
        print('content' in request.POST)
        if 'content' in request.POST:
            review.store_answer = request.POST['content']
            review.save()
            review = Review.objects.get(id=review_id)
            print(review.store_answer)
            messages.success(request, "Successfully answered review")
            return redirect('dashboard')
    else:
        messages.error(request, "Only store manager can answer reviews")
        return redirect('home')