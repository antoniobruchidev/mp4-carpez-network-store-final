from django.urls import path
from . import views

urlpatterns = [
    path('add_review', views.add_review, name='add_review'),
    path(
        'answer_review/<review_id>/',
        views.answer_review,
        name='answer_review',
    )
]
