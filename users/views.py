from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from loguru import logger


class ProfileDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logger.debug(context)
        context['user'] = self.request.user
        logger.debug(context['user'])
        return context
