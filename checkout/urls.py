from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
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
    ) 
]
