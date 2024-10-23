import uuid
from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Dashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    points = models.IntegerField(null=False, default=0)
    activation_url = models.CharField(max_length=80, null=True, blank=True)
    activated = models.BooleanField(default=False, null=False)
    
    def generate_activation_url(self):
        """Generate a random unique order number"""
        self.activation_url = uuid.uuid4().hex.upper()
        self.save()
    
    def save(self, *args, **kwargs):
        """
        Ovverride the original save method to set the activation url
        """
        if not self.activation_url:
            self.activation_url = self.generate_activation_url()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.user.username

