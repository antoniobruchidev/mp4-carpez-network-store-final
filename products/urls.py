from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_products, name='get_products'),
    path(
        'product_details/<product_id>',
        views.get_product_details,
        name='get_product_details'
    ),
    path('add_product', views.add_product, name='add_product'),
]
