# reviews application

Application that handles product reviews, it has two views: add_review and answer_review

## Development

### vscode terminal
```python
python manage.py createapp reviews
```

### '/ecommerce/settings.py'
```python
INSTALLED_APPS = [
    ...
    'reviews',
    ...
]
```

### '/reviews/urls.py'
```python
urlpatterns = [
    path('add_review', views.add_review, name='add_review'),
    path(
        'answer_review/<review_id>/',
        views.answer_review,
        name='answer_review',
    )
]
```

### '/ecommerce/urls.py'
```python
urlpatterns = [
    ...
    path('', include('reviews.urls')),
    ...
]
```

## Why
Review has a OneToOne field connected to OrderLineItem, with a receiver for every OrderLineItem created the app spans the associated Review with empty values.
Registered users who bought the items will have the review ready to be filled in their dashboard. When an user submits a review and gives a rating to the prooduct the app will make the average for that product and set it as the product rating.

## Testing

### add_review
- This view can be called by the user from its dashboard selecting a product to review from the dropdown.
- It display the form to be compiled.
- It updates both the review and the product rating.

### answer_review
- This view can be called by a superuser from its dashboard in the reviews tab.
- It successfully update the review with the store answer.
