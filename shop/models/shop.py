import uuid
from pathlib import Path
from typing import override

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

__all__ = ['Shop', 'ShopFollower']


def legal_id_upload_to(instance: 'Shop', filename: str):
    """
    Generator function specifying where to upload the
    shop client owner's verification ID.

    TODO: Update path since will point to auth user model.
    """
    # Get the filename's extension. (".jpg", ".png", ".pdf", etc.)
    ext = Path(filename).suffix.lower()

    # Organize path on where this media file will be uploaded.
    return f'clients/{instance.client.user.username}/uploads/legal-id{ext}'


def document_upload_to(instance: 'Shop', filename: str):
    """
    Generator function specifying where to upload the
    shop client owner's verification document.

    TODO: Update path since will point to auth user model.
    """
    # Get the filename's extension. (".pdf")
    ext = Path(filename).suffix.lower()

    # Organize path on where this media file will be uploaded.
    return (
        f'clients/{instance.client.user.username}'
        f'/uploads/business-permit{ext}'
    )


class Shop(models.Model):
    """
    Model representing a shop owned by a client.

    TODO: Add field(s) for social links (e.g. "X", "Facebook", etc.)
    """
    # Unique Identifier for the Shop
    # TODO: To make unique shop "name" field after this.
    shop_id = models.UUIDField(
        editable=False,
        default=uuid.uuid4,
        unique=True,
        verbose_name='Shop ID'
    )

    # Client Owner of the Shop
    # TODO: To point "settings.AUTH_USER_MODEL" as foreign key.
    client = models.OneToOneField(
        'users.Client',
        on_delete=models.CASCADE,
        related_name='shop',
        to_field='client_number',
        verbose_name='Shop Owner',
        help_text='The client who owns the shop.'
    )

    # Future Enhancement: Payout account for shop owner(s).
    # payout_account = models.OneToOneField(
    #     'billing.PayoutAccount',
    #     on_delete=models.CASCADE,
    #     default=None,
    #     null=True,
    #     blank=True,
    #     related_name='shop',
    #     verbose_name='Shop Payout Account',
    #     help_text='Bank account details for payouts.'
    # )

    # Shop Details
    description = models.TextField(
        blank=True,
        null=True,
        help_text='A brief description of the shop.'
    )

    # Follower Counts
    # NOTE: For de-normalization for optimization.
    follower_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Followers Count'
    )

    # Verification Field(s)
    legal_id = models.FileField(
        upload_to=legal_id_upload_to,
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=[
                'pdf', 'jpg', 'jpeg', 'png'
            ])
        ],
        verbose_name='Legal ID',
        help_text=(
            'Upload a legal ID for shop owner verification. '
            '(Allowed Types: ".pdf", ".jpg", ".jpeg", ".png")'
        )
    )
    verification_document = models.FileField(
        upload_to=document_upload_to,
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf'])
        ],
        verbose_name='Verification Document',
        help_text=(
            'Upload a PDF document for shop verification. '
            '(e.g., DTI Permit)'
        )
    )

    # Shop Status
    is_active = models.BooleanField(
        default=False,
        verbose_name='Active',
        help_text='Indicates whether the shop is verified and active.'
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

    @override
    def clean(self):
        """
        Custom validation for `Shop` model field(s).
        """
        # Invoke the base `clean()` method.
        super().clean()

        # Define a max file upload size.
        MAX_UPLOAD_SIZE = 10
        MAX_UPLOAD_MB = MAX_UPLOAD_SIZE * 1024 * 1024

        # Do a verification on the verification document.
        if self.verification_document:
            if self.verification_document.size > MAX_UPLOAD_MB:
                raise ValidationError(
                    'Verification document file size should '
                    f'not exceed {MAX_UPLOAD_SIZE}MB.'
                )

        # Do a verification on the legal id.
        if self.legal_id:
            if self.legal_id.size > MAX_UPLOAD_MB:
                raise ValidationError(
                    'Legal ID file size should not exceed '
                    f'{MAX_UPLOAD_SIZE}MB.'
                )

    @override
    def __str__(self):
        return f'{self.client.client_number}'

    class Meta:
        ordering = ['-created_at', '-modified_at']
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'


class ShopFollower(models.Model):
    """
    Model representing a shop follower-following
    relationship between a client and a shop.
    """
    fk_client = models.ForeignKey(
        'users.Client',
        on_delete=models.CASCADE,
        related_name='shops_followed',
        verbose_name='Client',
        help_text='The client who follows the shop.'
    )
    fk_shop = models.ForeignKey(
        'shop.Shop',
        on_delete=models.CASCADE,
        related_name='followers',
        to_field='shop_id',
        verbose_name='Shop',
        help_text='The shop being followed.'
    )
    date_followed = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date Followed'
    )

    @override
    def __str__(self):
        return f'{self.fk_client.display_name} - {self.fk_shop}'

    class Meta:
        ordering = ['-date_followed']
        unique_together = ('fk_client', 'fk_shop')
