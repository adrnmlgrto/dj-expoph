from django.contrib.auth import get_user_model
from django.db import transaction
from loguru import logger

from core.decorators.validate import validate_params
from core.handlers import resize_image_file_handler

from .schemas import RegisterStaffUser, RegisterUser

__all__ = [
    'register_user',
    'register_staff_user'
]


def _register_user(
    email: str,
    password: str,
    is_staff: bool = False,
    **extras
):
    """
    Helper function to register a user or staff into the system.

    Args:
        email (str): Email address of the user.
        password (str): Password for the user.
        is_staff (bool): Indicates that user is a staff. Defaults to False.
        **extras: Additional optional parameters for user registration.

    Returns:
        CustomUser: The created custom user object.
    """
    # Get the user model class.
    User = get_user_model()

    # Encapsulate the creation process within an atomic transaction
    # to enable rollback(s) when an unexpected error occurs.
    with transaction.atomic():

        # Create either a normal user or a staff user
        # based on the `is_staff` flag.
        if is_staff:
            user = User.objects.create_staff(
                email=email,
                password=password,
                **extras
            )
        else:
            user = User.objects.create_user(
                email=email,
                password=password,
                **extras
            )

        # Get `avatar` from the params, if passed.
        avatar = extras.get('avatar')

        # Process the avatar file if passed via a handler, then save.
        if avatar:
            avatar_img = resize_image_file_handler(avatar)
            user.avatar.save(avatar_img.name, avatar_img)

    # Log the event.
    logger.success(
        f'Successfully registered {'staff ' if is_staff else ''}'
        f'{user.email} ({user.display_name})'
    )

    return user


@validate_params(RegisterUser)
def register_user(email: str, password: str, **extras):
    """
    Register a standard user into the system.
    """
    return _register_user(email, password, is_staff=False, **extras)


@validate_params(RegisterStaffUser)
def register_staff_user(email: str, password: str, **extras):
    """
    Register a staff user into the system.
    """
    return _register_user(email, password, is_staff=True, **extras)
