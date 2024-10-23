from django.db.models.signals import post_save

from django.dispatch import receiver

from dashboard.models import User
from .views import request_email_signup


@receiver(post_save, sender=User)
def send_email_confirmation(sender, instance, created, **kwargs):
    """
        Send email signup confirmation
    """
    if created:
        request_email_signup(sender.id)
