from pathlib import Path
from typing import override

from django.contrib.auth.models import User
from django.db import models
from loguru import logger

from .utils import UserStatus, generate_client_number

__all__ = ['Client']


def avatar_upload_to(instance: 'Client', filename: str):
    """
    Generator function specifying where to upload client's avatar.
    """
    # Get the filename's extension. (".jpg", ".png", etc.)
    ext = Path(filename).suffix.lower()

    # Organize path on where this media file will be uploaded.
    return f'clients/{instance.user.username}/avatar{ext}'


class Client(models.Model):
    """
    Profile model for clients or customers.

    TODO: Use `twiliio` for SMS verification process. (09/18/2024)
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='client'
    )

    # Unique identification number.
    client_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        verbose_name='Client Number'
    )

    # Profile Details
    avatar = models.ImageField(
        upload_to=avatar_upload_to,
        null=True,
        blank=True,
        default=None
    )
    display_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Display Name'
    )
    mobile_number = models.CharField(
        max_length=20,
        verbose_name='Mobile Number'
    )
    shipping_address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Shipping Address',
        help_text=(
            'Required when buying physical merchandise(s).'
        )
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
    is_sms_verified = models.BooleanField(
        default=False,
        verbose_name='SMS Verified',
        help_text=(
            'For determining if client\'s mobile number '
            'is valid or not.'
        )
    )

    # Newsletter Subscription(s)
    newsletter = models.BooleanField(
        default=False
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
    def status(self) -> str:
        """
        Property that returns the status of the client.
        """
        STATUS_MAP = {
            (True, True): UserStatus.ACTIVE,
            (True, False): UserStatus.PENDING,
            (False, True): UserStatus.SUSPENDED,
            (False, False): UserStatus.UNKNOWN
        }
        return STATUS_MAP[(self.is_active, self.is_verified)]

    def follow_shop(self, shop_id: str) -> None:
        """
        Follow a specific shop given a `shop_id` string.
        """
        from shop.models.shop import Shop

        if self.shops_followed.filter(
            fk_shop__shop_id=shop_id
        ).exists():
            logger.warning(
                f'{self.display_name} is already following "{shop_id}".'
            )
            return  # do nothing as they follow already

        # Follow the shop by creating a `ShopFollower` instance.
        shop = Shop.objects.get(shop_id=shop_id)
        self.shops_followed.create(fk_shop=shop)
        logger.success(
            f'{self.display_name} followed "{shop_id}" successfully!'
        )

    def unfollow_shop(self, shop_id: str) -> None:
        """
        Unfollow a specific shop given a `shop_id` string.
        """
        if self.shops_followed.filter(
            fk_shop__shop_id=shop_id
        ).exists() is False:
            logger.warning(
                f'{self.display_name} isn\'t following "{shop_id}".'
            )
            return  # do nothing as they aren't even followed

        # Unfollow the shop followed by client
        # by deleting the `ShopFollower` instance.
        shop_to_delete = self.shops_followed.get(
            fk_shop__shop_id=shop_id
        )
        shop_to_delete.delete()
        logger.success(
            f'{self.display_name} unfollowed "{shop_id}" successfully!'
        )

    def set_status(self, status: UserStatus | str) -> None:
        """
        Set / update a client's current status.
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
    def save(self, *args, **kwargs):
        """
        Overridden save method for the `Client` model.
        """
        # Set the client number on creation.
        if self._state.adding and not self.client_number:
            self.client_number = generate_client_number()

        # When display name isn't set, use `User.username`.
        if not self.display_name:
            self.display_name = self.user.username

        # Save the client model instance.
        super().save(*args, **kwargs)

    @override
    def __str__(self):
        return f'{self.display_name}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
