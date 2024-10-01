from typing import override

from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    UserChangeForm,
    UserCreationForm,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from loguru import logger

from .models import CustomUser
from .models.utils import UserStatus


class CustomUserCreationForm(UserCreationForm):
    """
    A form for creating new users with email authentication.
    """
    class Meta:
        model = CustomUser
        fields = ('email',)
        field_classes = {
            'email': forms.EmailField
        }

    def clean_email(self):
        """
        Validate that the email is not already in use.
        """
        email = self.cleaned_data['email'].lower()
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError(_('This email is already registered.'))
        return email


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)
        field_classes = {
            'email': forms.EmailField
        }


class CustomAuthenticationForm(AuthenticationForm):
    """
    A form for authenticating users by their email and password.
    """
    username = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(
            attrs={
                'autocomplete': 'email',
                'autofocus': True
            }
        ),
    )

    @override
    def confirm_login_allowed(self, user: CustomUser):
        """
        Controls whether the given User may log in.
        """
        logger.debug('LOGGING IN')
        if user.status == UserStatus.PENDING:
            logger.debug('UNVERIFIED USER ATTEMPTED TO LOGIN')
            raise ValidationError(
                _('This account is currently unverified. '
                  'Please verify your account first before logging in.')
            )

        if user.status == UserStatus.SUSPENDED:
            logger.debug('SUSPENDED USER ATTEMPTED TO LOGIN')
            raise ValidationError(
                _('This account is currently suspended. '
                  'Please contact customer support for more information.')
            )

        if user.status == UserStatus.UNKNOWN:
            logger.debug('UNKNOWN USER ATTEMPTED TO LOGIN')
            raise ValidationError(
                _('Something went wrong while logging in. '
                  'Please contact the system administrator.')
            )


class CustomPasswordResetForm(PasswordResetForm):
    """
    A form for initiating the password reset process.
    """
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if CustomUser.objects.filter(email=email).exists():
            return email
        raise ValidationError(_('This email is not registered.'))


class CustomSetPasswordForm(SetPasswordForm):
    """
    A form for setting the password.
    """
    pass
