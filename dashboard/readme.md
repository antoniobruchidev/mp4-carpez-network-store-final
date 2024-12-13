# dashboard application
Application that handles superuser and user dashboards. It comprehends 11 views, dashboard will serve for both the superuser and the user dashboard pages while the other 10 will be called by the superuser dashboard to add and remove tags, brands, categories and discounts. It will have a searchbox where admin can enter an order number or a product sku, and 4 tabs, Orders, Reviews, Tags Brands and Categories, and finally Discounts.
Orders tab will show all the orders, paginated by 20 per page. on every order the admin can click on the order to see it in full and change the status.
Reviews tab will show the reviews which are still unaswered, giving the admin the possibility to answer publicly, or send a private email.
Tags, Brands and Categories will let the admin to add and delete any of those.
Discounts will let the admin add and delete discounts.

When accessed by a normal user it will display its points, a list of the orders done and the reviews he has not filled yet.

## Development

### vscode terminal
```python
python manage.py createapp dashboard
```

### '/ecommerce/settings.py'
```python
INSTALLED_APPS = [
    ...
    'dashboard',
    ...
]
```

### '/dashboard/urls.py'
```python
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add_tag', views.add_tag, name='add_tag'),
    path('add_brand', views.add_brand, name='add_brand'),
    path('add_category', views.add_category, name='add_category'),
    path('add_discount', views.add_discount, name='add_discount'),
    path('delete_discount/<discount_id>', views.delete_discount, name='delete_discount'),
    path('delete_brand/<brand_id>', views.delete_brand, name='delete_brand'),
    path('delete_category/<category_id>', views.delete_category, name='delete_category'),
    path('delete_tag/<tag_id>', views.delete_tag, name='delete_tag'),
    path('edit_order/<order_id>', views.edit_order, name='edit_order'),
    path('update_carousel/<tag_id>', views.change_carousel_tag, name='change_carousel_tag'),
]
```

### '/ecommerce/urls.py'
```python
urlpatterns = [
    ...
    path('', include('dashboard.urls')),
    ...
]
```



## Testing

### dashboard
- It displays different pages dependeing if user is superuser or not, not accessible if user is not logged in.
- If user it successfully retrieve the reviews the user still has not filled.
- If user it successfully displays the points.
- If user it successfully displays the list of submitted orders.
- If admin it successfully query for a single order_number or a single sku. if none is found it successfully notify the admin.
- If admin it sussessfully paginates and displays the order list.
- It successfully redirect the admin to to checkout_success page for that order displaying all the information about the order.
- It successfully displays the current status, it successfully update the status which successfully send email notification.
- If admin it successfully filter the reviews to be shown, exclude the ones that have not been filled and filter for those who haven't been answered yet.
- It successfully let the admin post an answer by clicling the paper plane button, and it successfully open the user email provider to compose an email by clicling the mail button.
- It admin post an answer it successfully notify him back and remove the review from the DOM.
- Badges tab successfully displays the badges by model, showing a popover on each one of them for the instructions.
- It successfully add tags, brands and categories, adding them to the DOM without reloading.
- It successfully delete tags from, brands and categories, also removing them from the DOM without reloading.
- If a tag cannot be deleted it shows the reason accordingly.
- The Discounts tabs successfully let the admin add and remove discounts notifying him back without reloading.

#### bugs
Removing a discount will set the discount to null in the Order model, which will not impact the grand_total that is set by the update_total method. But it won't be displayed in the order page. I will add a bool available to it, and instead of deleting them i will make them unavailable.


