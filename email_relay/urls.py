from django.urls import path
from . import views

urlpatterns = [
    path('send_email', views.send_confirmation_email, name="send_confirmation_email"),
]