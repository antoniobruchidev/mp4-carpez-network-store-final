# checkout application

It comprehend 4 views and a webhook: checkout, place_order, checkout_success and cache_checkout_data. It is responsobile for the flow of the checkout process

## Development

### vscode terminal
```python
python manage.py createapp checkout
```

### '/ecommerce/settings.py'
```python
INSTALLED_APPS = [
    ...
    'checkout',
    ...
]
```

### '/checkout/urls.py'
```python
urlpatterns = [
    path('<discount_id>', views.checkout, name='checkout'),
    path(
        'cache_checkout_data/',
        views.cache_checkout_data,
        name="cache_checkout_data"
    ),
    path(
        'place_order/',
        views.place_order,
        name='place_order'
    ),
    path(
        'checkout_success/<order_number>',
        views.checkout_success,
        name='checkout_success'
    ),
    path('wh/', webhook, name='webhook')
]
```

### '/ecommerce/urls.py'
```python
urlpatterns = [
    ...
    path('checkout/', include('checkout.urls')),
    ...
]
```

## Testing

### checkout
- It will display every item in the shopping cart each one of them with their quantities prices and subtotals, if a product has a discounted price it will show that.
- It will display a discount on the total if present.
- It is not possible for the user to submit the payment form without entering a valid email address into the email field.
- Shipping, billing and payment elements are part of the Stripe SDK. User can complete the payment entering the required inputs (Email, Full Name, Address) and use a Stripe development card or access the link element, which will save the user cards and the user addressess.
- It calls the cache_checkout_data view to have the backend add a bunch of metadata to the given payment intent.
- If the stripe payment succedes, the javascript will post to the place_order view data needed to create the order and on success it will redirect to checkout_success, if it doesn't it will display the user why it didn't.
- Using the reset button it resets only the email fields as the others are part of the shipping, billing and payment stripe elements. Leave as it is.

### cache_checkout_data
- It's called during the payment process to add a bunch of data to the json data that stripe will send back to our webhook to confirm the payment.
- It adds the desired data and respond as expected.

### place_order
- It checks the posted data and the current bag from context.
- It tries to find corresponding order, if it doesn't it creates it.
- If it finds the order it applies the user and the discount if present.
- If it creates the order, it will iterate through the shopping cart for every item creating an order line item and adding all of them to the order.
- Both the update_total method from Order model and save method from OrderLineModel take care of eventual discounts when present.
- If in any of the iteration of adding line items doesn't find the given product it should raise an error but it never happened yet.
- If a profile and a profile is present it applies them to the order.

### remove_from_bag
- It displays the information relative to the completed order.

### webhook
- Depending on the data it calls the right handler.
- It checks for the data posted
- It tries to find the corresponding order for 5 attempts. If it finds it changes the status to confirmed.
- It sets back the profile points to be used at 0.
- It sends the confirmation email
- It it doesn' find the order, it creates it.
- If a user is in the metadata we added in cache_checkout_data it will add the user. Same for the discount.
- It adds line items to the created order.
- It answer the stripe server accordingly.

