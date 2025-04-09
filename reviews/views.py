from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST

from checkout.models import OrderLineItem
from products.models import Product
from reviews.forms import ReviewForm
from reviews.models import Review
from django.contrib import messages


@require_http_methods(["GET", "POST"])
def add_review(request):
    if request.GET:
        if "lineitem" in request.GET:
            order_lineitem_id = int(request.GET["lineitem"])
            lineitem = get_object_or_404(OrderLineItem, id=order_lineitem_id)
            review = Review.objects.get(order=lineitem)
            form = ReviewForm(instance=review)
            template = "reviews/add_review.html"
            context = {"lineitem": lineitem, "form": form}
            return render(request, template, context)
        else:
            messages.error(request, "It was not specisified a product to review")
            return redirect("dashboard")
    else:
        order_lineitem_id = int(request.POST.get("lineitem"))
        lineitem = get_object_or_404(OrderLineItem, id=order_lineitem_id)
        review = Review.objects.get(order=lineitem)
        review.title = request.POST.get("title")
        review.content = request.POST.get("content")
        if int(request.POST.get("rating")) < 0:
            rating = 0
        elif int(request.POST.get("rating")) > 5:
            rating = 5
        else:
            rating = int(request.POST.get("rating"))
        review.rating = rating
        review.add_date()
        review.save()
        reviews = Review.objects.all()
        reviews_count = 0
        reviews_total = 0
        for review in reviews:
            order_lineitem = OrderLineItem.objects.get(review=review)
            if order_lineitem.product.id == lineitem.product.id:
                if review.rating is not None:
                    reviews_count += 1
                    reviews_total += review.rating
        rating = round(reviews_total / reviews_count, 1)
        product = get_object_or_404(Product, id=lineitem.product.id)
        product.rating = rating
        product.save()

        messages.success(
            request,
            f"You successfully reviewed product \
            {lineitem.product.name} ",
        )
        return redirect("dashboard")


@require_POST
def answer_review(request, review_id):
    data = dict()
    if request.user.is_superuser:
        try:
            review = Review.objects.get(id=review_id)
            if "content" in request.POST:
                review.store_answer = request.POST["content"]
                review.save()
                review = Review.objects.get(id=review_id)
                data["success"] = "Successfully answered review"
                status = 200
            else:
                data["error"] = "Answer could not be added, invalid inputs"
                status = 422
        except Exception as error:
            data["error"] = error.__str__()
            status = 500
        except Review.DoesNotExist:
            data["error"] = "Review could not be found"
            status = 404
        return JsonResponse(data=data, status=status)
    else:
        data["error"] = "Permission denied"
        return JsonResponse(data=data, status=403)
