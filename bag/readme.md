# Bag application

It comprehend 4 views for a simple and easy to use interface, view_bag, add_to_bag, update_item_quantity and remove_from_bag.

## Development

### vscode terminal
```python
python manage.py createapp bag
```

### '/ecommerce/settings.py'
```python
INSTALLED_APPS = [
    ...
    'bag',
    ...
]
```

### '/bag/urls.py'
```python
urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add/<product_id>', views.add_to_bag, name='add_to_bag'),
    path(
        'update/<product_id>',
        views.update_item_quantity,
        name='update_item_quantity'
    ),
    path(
        'remove/<product_id>',
        views.remove_from_bag,
        name='remove_from_bag'
        ),
]
```

### '/ecommerce/urls.py'
```python
urlpatterns = [
    ...
    path('bag/', include('bag.urls')),
    ...
]
```

## Testing

### view_bag
- User will be redirected to this view by clicking on the shopping cart button in the login/register dropdown or by clicking the button on the toast after adding a product to cart.
- It will display the content of the shopping cart as a table with product image, product name, action button arround the quantities and the subtotal.
- On a mobile device the image is hidden, text and buttons smaller so it can fit.
- Using increment and decrement buttons will set the maximum and minimum at 99 and 0.
- Removing the product will act as expected.
- Clicking on the use points checkox will enable the discounts available, user are shown only discounts for which they have enough points.
- If the user has selected a discount this will be forwarded to the checkout view


### update_item_quantity
- Updating to a negative number as quantity will redirect to the same shopping cart page displaying the error.
- Updating to a number bigger than 99 will update the item quantity as 99 and show message accordingly.
- Updating to 0 will act as expected.

### add_to_bag
- Every add to cart button present in the platform will redirect to this view, it act as expected.

### remove_from_bag
- Removing an item from the bag act as expected.

## Solved bugs

In case of both discount and delivery fees present it would create two different orders in place_order and in the webhook, in the bag context processor I was calculating the discount from total excluded delivery fees, while in checkout they were included in the total before calculating the discount. Even if the pid was the same, the amount of the transaction was different so I had two orders for the same transaction. Fixed by calculating the discount in the bag context processor from the grand total.

