from io import BytesIO

from django.core.files.base import ContentFile
from django.db.models import ImageField
from PIL import Image


def resize_image_handler(
    image_field: ImageField,
    size: tuple[int, int] = (300, 300),
    quality: int = 85
):
    """
    Resize and compress the image before saving.

    Args:
        image_field (ImageField): The uploaded image file.
        size (tuple): The target size to resize to (width, height).
        quality (int): The quality of the image after compression (1-100).

    Returns:
        ContentFile: The processed image as a file ready to be saved.
    """
    img = Image.open(image_field)

    # Convert to RGB to ensure no issues with formats like PNG.
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    # Resize the image.
    img.thumbnail(size, Image.Resampling.LANCZOS)

    # Save the resized image to a BytesIO object.
    img_io = BytesIO()
    img.save(img_io, format='JPEG', quality=quality)

    # Create a Django ContentFile object for saving.
    return ContentFile(img_io.getvalue(), name=image_field.name)
