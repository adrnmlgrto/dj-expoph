from typing import override

from django.db import models

__all__ = ['Shop', 'ShopFollower']


class Shop(models.Model):
    """
    Model representing a shop owned by a client.
    """
    # Client Owner of the Shop
    owner = models.OneToOneField(
        'users.Client',
        on_delete=models.CASCADE,
        related_name='shop',
        verbose_name='Shop Owner'
    )

    # Future Enhancement: Bank account for payout(s).
    # bank_account = models.OneToOneField(
    #     'billing.BankAccount',
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True,
    #     related_name='shop',
    #     verbose_name='Bank Account',
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
    # TODO: Add increment/decrement on signals
    # on `ShopFollower` create/delete.
    follower_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Store Follower Count'
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
    def __str__(self):
        return f'{self.owner.display_name}'

    class Meta:
        ordering = ['-created_at']
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
        related_name='shops_followed'
    )
    fk_shop = models.ForeignKey(
        'shop.Shop',
        on_delete=models.CASCADE,
        related_name='followers'
    )
    date_followed = models.DateTimeField(
        auto_now_add=True
    )
