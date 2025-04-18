import uuid
from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


class Dashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    points = models.IntegerField(null=False, default=0)
    in_use = models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or Update the user profile
    """
    if created:
        Dashboard.objects.create(user=instance)
    instance.dashboard.save()
