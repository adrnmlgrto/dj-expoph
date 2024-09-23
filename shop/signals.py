from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models.shop import ShopFollower


@receiver(post_save, sender=ShopFollower)
def increment_follower_count(
    sender, instance: ShopFollower, created, **kwargs
):
    """
    Increments the shop's total follower count
    upon creating a `ShopFollower` instance.
    """
    if created:
        instance.fk_shop.follower_count += 1
        instance.fk_shop.save()


@receiver(post_delete, sender=ShopFollower)
def decrement_follower_count(
    sender, instance: ShopFollower, **kwargs
):
    """
    Decrements the shop's total follower count
    upon creating a `ShopFollower` instance.
    """
    instance.fk_shop.follower_count -= 1
    instance.fk_shop.save()
