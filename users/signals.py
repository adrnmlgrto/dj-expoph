from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Admin
from .models.utils import generate_admin_number


@receiver(pre_save, sender=Admin)
def set_admin_number(sender, instance: Admin, **kwargs):
    """
    Signal handler to set the admin number before saving.
    """
    # Only generate the admin number if it hasn't been set.
    if not instance.admin_number:
        instance.admin_number = generate_admin_number(
            instance.department
        )
