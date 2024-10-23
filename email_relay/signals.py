from django.db.models.signals import post_save

from django.dispatch import receiver

from dashboard.models import Dashboard
from .views import request_email_signup


@receiver(post_save, sender=Dashboard)
def send_email_confirmation(sender, instance, created, **kwargs):
    """
        Send email signup confirmation
    """
    if created:
        user = sender.user
        request_email_signup(user.id)

   