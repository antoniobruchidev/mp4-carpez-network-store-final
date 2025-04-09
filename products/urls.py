from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_products, name="get_products"),
    path(
        "product_details/<product_id>",
        views.get_product_details,
        name="get_product_details",
    ),
    path("add_product", views.add_product, name="add_product"),
    path(
        "edit_product_details/<product_id>",
        views.edit_product_details,
        name="edit_product_details",
    ),
    path("delete_product/<product_id>", views.delete_product, name="delete_product"),
]
