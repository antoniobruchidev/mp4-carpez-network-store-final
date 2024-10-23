from django.urls import path
from . import views

urlpatterns = [
    path('send_email', views.send_confirmation_email, name="send_confirmation_email"),
    path('send/<order_id>', views.try_email, name='try_email'),
]