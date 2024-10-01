from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from loguru import logger


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
