from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


__all__ = ['CustomUserManager']


class CustomUserManager(BaseUserManager):
    """
    The manager class for a custom user model.

    This model manager makes use of the custom user's `email` field
    as the unique identifier for authentication instead of the
    default `username` field.
    """
    def create_user(
        self, email: str, password: str = None, **extra_fields
    ):
        """
        Create and save a user with the given email and password.

        Args:
            email: The email to set for the user.
            password: The password to set for the user. Defaults to None.
                When this field is None, it sets an unusable
                password for the custom user instance.
            **extra_fields: Extra field parameters for creating a user.
                This can include fields such as `is_staff`, `is_active`, etc.
                For reference, please see Django's `User` fields.

        Returns:
            CustomUser: A created instance of the custom user model.

        Raises:
            ValueError: If `email` is not set or is None.
        """
        # Make sure that the email is passed as an argument.
        if not email:
            raise ValueError(_('The email must be set'))

        # Normalize the email's domain, lowercasing it.
        email = self.normalize_email(email)

        # Initialize the custom user model, and set the password.
        # NOTE: When a password isn't passed, it sets an unusable password.
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_staff(
        self, email: str, password: str = None, **extra_fields
    ):
        """
        Create and save a staff user with the given email and password.

        Args:
            email: The email to set for the staff user.
            password: The password to set for the staff user. Defaults to None.
                When this field is None, it sets an unusable
                password for the custom user instance.
            **extra_fields: Extra field parameters for creating a staff user.
                This can include fields such as `is_staff`, `is_active`, etc.
                For reference, please see Django's `User` fields.

        Returns:
            CustomUser: A created staff user instance of the custom user model.

        Raises:
            ValueError: If `email` is not set or is None, or when `is_staff`
                is False, or when `is_superuser` is set to True.
        """
        # Set defaults for the boolean fields for a staff user.
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)

        # Validate the boolean fields needed for a staff user.
        if extra_fields.get('is_superuser') is True:
            raise ValueError(_('Superuser must have is_superuser=False.'))
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))

        return self.create_user(email, password, **extra_fields)

    def create_superuser(
        self, email: str, password: str = None, **extra_fields
    ):
        """
        Create and save a super user with the given email and password.

        Args:
            email: The email to set for the superuser.
            password: The password to set for the superuser. Defaults to None.
                When this field is None, it sets an unusable
                password for the custom user instance.
            **extra_fields: Extra field parameters for creating a superuser.
                This can include fields such as `is_staff`, `is_active`, etc.
                For reference, please see Django's `User` fields.

        Returns:
            CustomUser: A created superuser instance of the custom user model.

        Raises:
            ValueError: If `email` is not set or is None, or when `is_staff`
                or `is_superuser` is False.
        """
        # Set defaults for the boolean fields for a super user.
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # Validate the boolean fields needed for a super user.
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)
