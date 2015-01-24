from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

from models import Employee, Company, Employment as ECM
from custom_auth.models import User

# We need to create an Employee profile when a new user is created.
def create_user_profile(sender, instance, created, **kwargs):
    """Create an Employee profile for a new user."""
    if created:
        Employee.objects.create(user=instance)

def create_user_token(sender, instance, created, **kwargs):
    """Create an authentication token when creating a new user."""
    if created:
        Token.objects.create(user=instance)

# Wire up signals
post_save.connect(create_user_profile, sender=User)
post_save.connect(create_user_token, sender=User)
