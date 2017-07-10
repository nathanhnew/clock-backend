from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import AccountSettings
from authorization.models import Account


@receiver(post_save, sender=Account)
def create_related_profile(sender, instance, created, *args, **kwargs):
    # Checking for 'created'. ONly want to call this function when
    # A new user is created.
    if instance and created:
        instance.settings = AccountSettings.objects.create(owner=instance)
