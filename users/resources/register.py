from django.contrib.auth.models import User
from django.db import transaction
from loguru import logger

from core.decorators.validate import validate_params
from core.handlers import resize_image_file_handler

from ..models import Admin, Client
from ..models.utils import Department
from .schemas import RegisterAdmin, RegisterClient

__all__ = [
    'register_admin',
    'register_client'
]


@validate_params(RegisterAdmin)
def register_admin(
    username: str,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    **extras
) -> Admin:
    """
    Register an administrator user account.

    This creates the actual `User` instance first,
    then proceeds to create our own record for the
    administrator along with their profile details.
    """
    # Encapsulate the creation process within atomic transaction
    # to enable rollback(s) when an unexpected error occurs.
    with transaction.atomic():

        # Get the department from extra kwargs.
        department = extras.get('department')

        # Create a superuser instance when the departmnent is `ADMIN`.
        if department == Department.ADMIN or department == 'sysadmin':
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
        # Create a "staff" user when not a system administrator.
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=True
            )

        # After creating the user, create the `Admin` instance.
        admin = Admin.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            department=department
        )

        # Get `avatar` on params, if passed.
        avatar = extras.get('avatar')

        # Process the avatar file if passed via a handler, then save.
        if avatar:
            avatar_img = resize_image_file_handler(avatar)
            admin.avatar.save(avatar_img.name, avatar_img)

    # Log the event onto the command line.
    logger.success(
        'Successfully registered administrator '
        f'"{admin.full_name}" ({user.username}).'
    )

    return admin


@validate_params(RegisterClient)
def register_client(
    username: str,
    email: str,
    password: str,
    mobile_number: str,
    **extras
) -> Client:
    """
    Register a client / customer account.

    This creates the actual `User` instance first,
    then proceeds to create our own record for the
    client along with their profile details.
    """
    # Encapsulate the creation process within atomic transaction
    # to enable rollback(s) when an unexpected error occurs.
    with transaction.atomic():

        # Create the user instance.
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # After creating the user, create the `Client` instance.
        client = Client.objects.create(
            user=user, mobile_number=mobile_number, **extras
        )

        # Get `avatar` on params, if passed.
        avatar = extras.get('avatar')

        # Process the avatar file if passed via a handler, then save.
        if avatar:
            avatar_img = resize_image_file_handler(avatar)
            client.avatar.save(avatar_img.name, avatar_img)

    # Log the event onto the command line.
    logger.success(
        f'Successfully registered "{client.display_name}" '
        f'({user.username}) client!'
    )

    return client
