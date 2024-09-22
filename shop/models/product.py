from django.db import models

__all__ = ['Product']


class Product(models.Model):
    """
    Model representing a shop's product.

    TODO: Implement product categories.
    """
    # TODO: Move to `./utils.py`
    DIGITAL = 'digital'
    PHYSICAL = 'physical'

    PRODUCT_TYPE_CHOICES = [
        (DIGITAL, 'Digital'),
        (PHYSICAL, 'Physical'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_type = models.CharField(
        max_length=10, choices=PRODUCT_TYPE_CHOICES, default=PHYSICAL
    )
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField(default=0)  # For physical products
    file = models.FileField(upload_to='digital_goods/', blank=True, null=True)  # For digital goods

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    # Add additional methods or metadata as necessary
