from io import BytesIO
from pathlib import Path
from typing import TypeVar, Union

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile
from django.db.models.fields.files import ImageFieldFile
from PIL import Image

# Declare the ImageFileType for the handler function.
ImageFileType = TypeVar(
    'ImageFileType',
    bound=Union[UploadedFile, ImageFieldFile]
)


def resize_image_file_handler(
    image_file: ImageFileType,
    size: tuple[int, int] = (300, 300),
    quality: int = 75
) -> ContentFile:
    """
    Handler that resizes and compresses an image file
    before saving.

    This process outputs a progressive `JPEG` content file that
    would be saved into the image file field of the model instance.

    The function accepts flexible input types for `image_file`,
    such as Django file objects (subclasses of `UploadedFile`).

    Args:
        image_file (ImageFileType): The uploaded image file or an \
            already saved image file.
        size (tuple): The target size to resize to (width, height).
        quality (int): The quality of the image after compression (1-100).

    Returns:
        ContentFile: The processed image as a file ready to be saved.
    """
    # Validations before doing any image processing.
    if not isinstance(image_file, UploadedFile):
        raise TypeError(
            'Param "image_file" should be a type '
            f'subclass of "{UploadedFile.__name__}".'
        )

    # Ensure the quality is between 0 and 95.
    if not (0 <= quality <= 95):
        raise ValueError('Quality must be between 0 and 95.')

    # Read the image and store as an `ImageFile` using `PIL.Image`.
    img = Image.open(image_file)

    # Convert to RGB to ensure no issues with formats like PNG.
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    # Resize the image using thumbnail.
    img.thumbnail(size, Image.Resampling.LANCZOS)

    # Save the resized image to a BytesIO object.
    # NOTE: Force save into a `JPEG` format for any image files.
    img_io = BytesIO()
    img.save(
        img_io,
        format='JPEG',
        quality=quality,
        optimize=True,  # optimize encoder
        progressive=True  # set as a progressive JPEG file
    )

    # Get filename from the image file.
    filename = image_file.name

    # Handle the file name when the passed image file is `ImageFieldFile`.
    # NOTE: Django stores it along with the relative path, so use `Path.name`
    if isinstance(image_file, ImageFieldFile):
        filename = Path(image_file.name).name

    # Create a Django ContentFile object for saving.
    return ContentFile(content=img_io.getvalue(), name=filename)
