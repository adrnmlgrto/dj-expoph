import sys

from django.contrib.auth.models import User
from django.db import transaction
from loguru import logger

from users.models import Admin, Client
from users.models.utils import Department

__all__ = [
    'register_admin',
    'register_client'
]

# Set the logger formatting.
logger.add(
    sink=sys.stdout,
    format="{time:MMMM D, YYYY > HH:mm:ss} | {level} | {message}"
)


@logger.catch
def register_admin(
    username: str,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    department: Department = Department.ADMIN
) -> Admin:
    """
    Register an administrator user account.

    This creates the actual `User` instance first,
    then proceeds to create our own record for the
    administrator along with their profile details.
    """
    # Do a quick check for the department argument passed.
    if department not in Department.values:
        raise ValueError(f'"{department}" is invalid.')

    # Encapsulate the creation process within atomic transaction
    # to enable rollback(s) when an unexpected error occurs.
    with transaction.atomic():

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

    # Log the event onto the command line.
    logger.info(
        'Successfully registered administrator '
        f'"{admin.full_name}" ({user.username}).'
    )

    return admin


@logger.catch
def register_client(
    username: str,
    email: str,
    password: str,
    mobile_number: str,
    display_name: str = None,
    shipping_address: str = None
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
            user=user,
            display_name=display_name,
            mobile_number=mobile_number,
            shipping_address=shipping_address
        )

    # Log the event onto the command line.
    logger.info(
        f'Successfully registered "{client.display_name}" '
        f'({user.username}) client!'
    )

    return client
