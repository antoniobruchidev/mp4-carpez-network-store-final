from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add_tag', views.add_tag, name='add_tag'),
    path('add_brand', views.add_brand, name='add_brand'),
    path('add_category', views.add_category, name='add_category'),
]