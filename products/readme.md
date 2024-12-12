# Product application

It comprehend 5 views for a simple and easy to use interface, get_products, get_product_details, add_product, edit_product_details and delete_product.

## Development

### vscode terminal
```python
python manage.py createapp products
```

### '/ecommerce/settings.py'
```python
INSTALLED_APPS = [
    ...
    'products',
    ...
]
```

### '/home/urls.py'
```python
urlpatterns = [
    path('', views.get_products, name='get_products'),
    path(
        'product_details/<product_id>',
        views.get_product_details,
        name='get_product_details'
    ),
    path('add_product', views.add_product, name='add_product'),
    path(
        'edit_product_details/<product_id>',
        views.edit_product_details,
        name='edit_product_details'
    ),
    path(
        'delete_product/<product_id>',
        views.delete_product,
        name='delete_product'
    ),
]
```

### '/ecommerce/urls.py'
```python
urlpatterns = [
    ...
    path('products/', include('products.urls')),
    ...
]
```

## Testing

### get_products
- Entering this view with no queries will result in a list of all available products in store if you are a normal or unregistered user, it will return every product if user is superuser.
- Clicking a Tag, Brand, Category badges across the platform will always redirect to this view which will return the associated products.
- Using the search box it will return a list of products which name, description or brand will contain the user query. It will not return doubles thanks to the distinct() call after filtering the queries.
- If sorting by rating it will exclude unrated product
- It is not possibile for the user to submit an empty query
- After clicking on a Tag the categories dropdown would not work since I was not passing the categories queryset to the context. Moved the tag filter at the end of the view befor adding discounted prices.
- If a product has a discount set it will show both prices with the old one crossed.
- If a product has a rating it will fill the stars accordingly.
- Clicking on the reviews button will show the reviews section
- Entering the view as superuser will have edit and delete buttons instead of add to cart button
- The edit button will redirect to the edit view.
- The delete button will open a modal which will ask for confirmation. All the modal button work accordingly.

### get_products_details
- It will display all the badges (brand, category and tags) associated with it under the name of the product.
- If a product has a discount set it will show both prices with the old one crossed.
- If a product has a rating it will fill the stars accordingly and display the reviews button.
- Clicking on the reviews button will show the reviews section.
- Entering the view as superuser will have edit and delete buttons instead of add to cart button.
- The edit button will redirect to the edit view.
- The delete button will open a modal which will ask for confirmation. All the modal button work accordingly.

### edit_product_details & add_product
- They successfully change product detils or create the product in the first place.
- It is not possible for the user to enter wrong type of inputs or leave required inputs empty.
- Tricky the selections of the tags, the user need to hold down 'ctrl' otherwise the new selection will remove the others. Leave as it is for now.
- The platform will notify the user if he try to upload a file that is not an image or that's corrupted. 
- The platform will notify to add required fields if missing.

### delete_product
- It deletes the given product or return a 404 error if the given product does not exist.

