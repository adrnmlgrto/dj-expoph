import random
import string
from pathlib import Path
from typing import override

from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _
from loguru import logger

from ..managers import CustomUserManager
from .utils import UserStatus

__all__ = ['CustomUser']


def avatar_upload_to(instance: 'CustomUser', filename: str):
    """
    Generator function specifying where to upload the user's avatar.
    TODO: Use internal `uid` of the custom user instance as folder name.
    """
    # Get the filename's extension. (".jpg", ".png", etc.)
    ext = Path(filename).suffix.lower()

    # Organize path on where this media file will be uploaded.
    return f'users/{instance.display_name}/avatar{ext}'


def default_display_name():
    """
    Generates a short, random display name consisting
    of a prefix and random letters/digits.

    Returns:
        str: The generated display name with the prefix.
    """
    characters = string.ascii_letters + string.digits
    random_str = ''.join(random.choice(characters) for _ in range(8))
    return f'user-{random_str}'


class CustomUser(AbstractUser):
    """
    The implementation of a customized `User` model.

    This model would omit the `username` field, and make the
    `email` field as the default field for authenticating
    the user.
    """
    # Set the custom user model manager.
    objects = CustomUserManager()

    # TODO: Need to add `uid` field for unique identification.
    # Remove username field, and make the email field unique.
    username = None
    email = models.EmailField(
        _('Email Address'),
        unique=True,
        validators=[validate_email]  # add additional validation if needed
    )

    # Add an optional avatar field for a user.
    avatar = models.ImageField(
        _('Avatar'),
        upload_to=avatar_upload_to,
        blank=True,
        null=True,
        default=None
    )

    # Add field `display_name` to set for this user.
    display_name = models.CharField(
        _('Display Name'),
        max_length=150,
        default=default_display_name
    )

    # Add additional boolean field for verified user(s).
    is_verified = models.BooleanField(
        _('Verified'),
        default=False,
        help_text=_(
            'Designates whether this user has been verified. '
            'This serves as an internal user check for the system.'
        )
    )

    # Timestamps
    created_at = models.DateTimeField(
        _('Created At'),
        auto_now_add=True
    )
    modified_at = models.DateTimeField(
        _('Modified At'),
        auto_now=True
    )

    # Set email as the authentication field.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['display_name']

    @property
    def status(self) -> UserStatus:
        """
        Property that returns the status label of the user.
        NOTE: Used only for the rendering of the status string.
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
        Set / update the user's current status.
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

    def follow_shop(self, shop_id: str) -> None:
        """
        Follow a specific shop given a `shop_id` string.

        TODO: Need to update the shop model to reference this user.
        """
        from shop.models.shop import Shop

        if self.shops_followed.filter(
            fk_shop__shop_id=shop_id
        ).exists():
            logger.warning(
                _(f'{self.display_name} is already following "{shop_id}".')
            )
            return  # do nothing as they follow already

        # Follow the shop by creating a `ShopFollower` instance.
        shop = Shop.objects.get(shop_id=shop_id)
        self.shops_followed.create(fk_shop=shop)
        logger.success(
            _(f'{self.display_name} followed "{shop_id}" successfully!')
        )

    def unfollow_shop(self, shop_id: str) -> None:
        """
        Unfollow a specific shop given a `shop_id` string.

        TODO: Need to update the shop model to reference this user.
        """
        if self.shops_followed.filter(
            fk_shop__shop_id=shop_id
        ).exists() is False:
            logger.warning(
                _(f'{self.display_name} isn\'t following "{shop_id}".')
            )
            return  # do nothing as they aren't even followed

        # Unfollow the shop followed by client
        # by deleting the `ShopFollower` instance.
        shop_to_delete = self.shops_followed.get(
            fk_shop__shop_id=shop_id
        )
        shop_to_delete.delete()
        logger.success(
            _(f'{self.display_name} unfollowed "{shop_id}" successfully!')
        )

    @override
    def __str__(self) -> str:
        return self.email

    class Meta:
        ordering = ['-created_at']
