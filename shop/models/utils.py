from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class ProductType(TextChoices):
    """
    Status choice(s) for product types.
    """
    DIGITAL = 'DIG', _('Digital')
    PHYSICAL = 'PHY', _('Physical')
