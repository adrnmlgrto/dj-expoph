from decimal import Decimal
from pathlib import Path
from typing import override

from django.db import models

from .utils import ProductType

__all__ = ['Product']


def product_file_upload_to(instance: 'Product', filename: str):
    """
    Generator function specifying where to upload
    the shop's product file.

    e.g. "shop_id/sku/product_name.png"
    """
    # Get the filename's extension. (".png", ".jpg", etc.)
    ext = Path(filename).suffix.lower()

    # Organize path on where this product's file will be uploaded.
    return (
        f'{instance.fk_shop.shop_id}/'
        f'{instance.sku}/{instance.name}_PRODUCT{ext}'
    )


def product_img_upload_to(instance: 'Product', filename: str):
    """
    Generator function specifying where to upload
    the product's image.
    """
    # Get the filename's extension. (".jpeg")
    ext = Path(filename).suffix.lower()

    # Organize path on where this product's image will be uploaded.
    # Amazon S3 will overwrite existing files with the same name.
    return (
        f'{instance.fk_shop.shop_id}/'
        f'{instance.sku}/{instance.name}_IMG{ext}'
    )


class Product(models.Model):
    """
    Model representing a shop's product.

    NOTE: Products can be either digital or physical.
    NOTE: Default currency to use is PHP (₱) or Philippine Peso.
    """
    # The shop that owns or sells this specific product.
    fk_shop = models.ForeignKey(
        'shop.Shop',
        on_delete=models.CASCADE,
        related_name='products',
        to_field='shop_id',
        help_text='The shop that owns / lists the product.',
        verbose_name='Shop'
    )

    # Product information field(s).
    sku = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        help_text=(
            'Unique Stock Keeping Unit (SKU) '
            'for product identification.'
        )
    )
    product_type = models.CharField(
        max_length=10,
        choices=ProductType.choices,
        default=ProductType.DIGITAL
    )
    name = models.CharField(
        max_length=255,
        help_text='The name of the product.',
        verbose_name='Name'
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text='The description of the product.',
        verbose_name='Description'
    )
    # TODO: Several media uploads for product.
    img = models.ImageField(
        upload_to=product_img_upload_to,
        blank=True,
        null=True,
        default=None,
        help_text='The image of the product.',
        verbose_name='Image'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='The price of the product. Defaults to ₱0.00.',
        verbose_name='Price'
    )

    # The actual digital product file. Set to null if physical.
    # TODO: Validate upon saving if product type is digital, this field
    # should not be null.
    file = models.FileField(
        upload_to=product_file_upload_to,
        blank=True,
        null=True,
        default=None
    )

    # Status of the product.
    is_listed = models.BooleanField(
        default=True,
        help_text='Designates whether this product is listed or not.',
        verbose_name='Listed'
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='The date and time when the product was created.',
        verbose_name='Created At'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='The date and time when the product was last updated.',
        verbose_name='Updated At'
    )

    @override
    def save(self, *args, **kwargs) -> None:
        """
        Overridden save method for the `Product` model.
        """
        # Set a default SKU when not provided.
        if not self.sku:

            # Create a unique SKU for each product.
            # Strip spaces and whitespaces from the shop name.
            shop_name = self.fk_shop.shop_name.replace(' ', '')
            shop_name = shop_name.replace('\n', '').replace('\r', '')

            # Set the SKU, make sure `pk` has padded 0s.
            # e.g. "XYZSHOP-PHY-000001"
            self.sku = (
                f'{shop_name}-{self.product_type.value}'
                f'-{str(self.pk).zfill(6)}'.upper()
            )

        # Save the product instance.
        super().save(*args, **kwargs)

    @override
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at', '-updated_at']


class ProductInventory(models.Model):
    """
    Inventory model representing the stock quantity of a product.

    NOTE: Do NOT automatically unlist a product when it's out of stock.
    """
    product = models.OneToOneField(
        'shop.Product',
        on_delete=models.CASCADE,
        related_name='inventory',
        verbose_name='Product',
        help_text='The product whose stock is being tracked.'
    )
    qty = models.PositiveIntegerField(
        default=0,
        verbose_name='Stock Quantity',
        help_text='The available quantity of the product in stock.'
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Last Updated'
    )

    # Analytics for products sold and revenue.
    # NOTE: Should only be visible to the shop owner.
    total_units_sold = models.PositiveIntegerField(
        default=0,
        verbose_name='Total Units Sold',
        help_text='The total number of units the product has sold.'
    )
    total_revenue = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='Total Revenue',
        help_text='The total revenue generated from the product.'
    )

    @property
    def is_in_stock(self) -> bool:
        """
        Property to check whether the product is in stock.

        Returns:
            bool: True if the product is in stock, False otherwise.
        """
        # Digital products are always in stock unless explicitly unlisted.
        if self.product.product_type == ProductType.DIGITAL:
            return self.product.is_listed

        # Physical products are in stock only if quantity > 0 and listed.
        elif self.product.product_type == ProductType.PHYSICAL:
            return self.qty > 0 and self.product.is_listed

        return False

    @override
    def __str__(self):
        return f'{self.product.name} - {self.qty} in stock'

    class Meta:
        verbose_name = 'Product Inventory'
        verbose_name_plural = 'Product Inventories'
