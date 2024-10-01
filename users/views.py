from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from loguru import logger

from .forms import (
    CustomAuthenticationForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    CustomUserCreationForm
)


class RegisterView(CreateView):
    """
    Class-based view to render the registration form.

    Attributes:
        template_name (str): Template used to render the registration form.
        form_class (type): Form used to register a new user.
        success_url (str): URL to redirect to after successful registration.
    """
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """
        Override the form_valid method to automatically log
        the user in after successful registration.

        Args:
            form (Form): Form used to register a new user.
        """
        # Save the new user, and log the user in.
        user = form.save()
        login(self.request, user)


class CustomLoginView(LoginView):
    """
    View to render the login form and handle authentication.

    Attributes:
        template_name (str): Template used to render the login form.
        authentication_form (Form): Form used to authenticate a user.
        redirect_authenticated_user (bool): Whether to redirect to the user
            after successful login.
    """
    template_name = 'users/login.html'
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True


class CustomPasswordResetView(PasswordResetView):
    """
    View to render the password reset form and handle password reset.

    TODO: Add email template html.

    Attributes:
        template_name (str): Template used to render the password reset form.
        form_class (Form): Form used to reset a user's password.
        success_url (str): URL to redirect to after successful password reset.
    """
    template_name = 'users/password_reset.html'
    form_class = CustomPasswordResetForm
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    View to render the password reset confirmation form and handle password
    reset confirmation.

    Attributes:
        template_name (str): Template used to render the password reset
            confirmation form.
        form_class (Form): Form used to confirm a user's password reset.
        success_url (str): URL to redirect to after successful password
            reset confirmation.
    """
    template_name = 'users/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('users:login')


class ProfileDashboardView(LoginRequiredMixin, TemplateView):
    """
    Class-based view to render the user's profile dashboard.

    Attributes:
        template_name (str): Template used to render the profile dashboard.
    """
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        """
        Override the context data to pass user data to the template.

        Returns:
            dict: Context data with user information.
        """
        # Get the logged in user from the request, and add to context data.
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user

        # Log [DEBUG] the user that is currently logged in.
        logger.debug(self.request.user.email)
        return context
