from django.urls import path
from . import views

urlpatterns = [
    path('receive_error/', views.receive_error, name='receive_error')
]