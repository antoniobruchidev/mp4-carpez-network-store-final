from django.db import models

from checkout.models import OrderLineItem

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Review(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    order = models.OneToOneField(OrderLineItem, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.order.product.name


@receiver(post_save, sender=OrderLineItem)
def create_or_update_review(sender, instance, created, **kwargs):
    """
        Create or Update the user profile
    """
    if created:
        Review.objects.create(order=instance)
    instance.review.save()
