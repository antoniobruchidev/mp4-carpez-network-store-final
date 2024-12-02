from django.urls import path
from . import views

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
]