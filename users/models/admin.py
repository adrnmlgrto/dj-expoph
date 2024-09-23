from pathlib import Path
from typing import override

from django.contrib.auth.models import User
from django.db import models

from .utils import Department, UserStatus

__all__ = ['Admin']


def avatar_upload_to(instance: 'Admin', filename: str):
    """
    Generator function specifying where to upload admin's avatar.
    """
    # Get the filename's extension. (".jpg", ".png", etc.)
    ext = Path(filename).suffix.lower()

    # Organize path on where this media file will be uploaded.
    return f'admins/{instance.admin_number}/avatar{ext}'


class Admin(models.Model):
    """
    Profile model for admin users on the system.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='admin'
    )

    # Unique identification number.
    admin_number = models.CharField(
        max_length=15,
        unique=True,
        editable=False,
        verbose_name='Admin Number'
    )

    # Department Details
    department = models.CharField(
        max_length=20,
        choices=Department.choices,
        default=Department.ADMIN,
        verbose_name='Department'
    )

    # Profile Details
    avatar = models.ImageField(
        upload_to=avatar_upload_to,
        null=True,
        blank=True,
        default=None
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name='First Name'
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Last Name'
    )

    # Statuses
    is_active = models.BooleanField(
        default=True,
        verbose_name='Active'
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name='Verified'
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Modified At'
    )

    @property
    def full_name(self) -> str:
        """
        Property for returning the admin user's full name.
        """
        return f'{self.first_name} {self.last_name}'

    @property
    def status(self) -> str:
        """
        Property that returns the status of the admin user.
        """
        STATUS_MAP = {
            (True, True): UserStatus.ACTIVE,
            (True, False): UserStatus.PENDING,
            (False, True): UserStatus.SUSPENDED,
            (False, False): UserStatus.UNKNOWN
        }
        return STATUS_MAP[(self.is_active, self.is_verified)]

    def set_status(self, status: UserStatus | str) -> None:
        """
        Set / update an admin user's current status.
        """
        # Define the mapping of user status to set to instance attrs.
        STATUS_TO_SET_MAP = {
            UserStatus.ACTIVE: (True, True),
            UserStatus.PENDING: (True, False),
            UserStatus.SUSPENDED: (False, True)
        }

        # Get appropriate status booleans from mapping.
        statuses = STATUS_TO_SET_MAP.get(status)

        # Raise error when an invalid status is passed.
        if not statuses:
            raise ValueError(f'Status "{status}" cannot be set.')

        # Unpack tuple then set status on instance.
        active, verified = statuses
        self.is_active = active
        self.is_verified = verified

        # Save the instance after updating statuses.
        # NOTE: This will update the `modified_at` timestamp.
        self.save()

    @override
    def __str__(self):
        return f'{self.admin_number}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'
