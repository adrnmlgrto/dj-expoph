from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy

from .views import ProfileDashboardView

urlpatterns = [
    path(
        'login/',
        LoginView.as_view(
            template_name='users/login.html',
            redirect_authenticated_user=True,
            success_url=reverse_lazy('profile_dashboard')
        ),
        name='login'
    ),
    path(
        'profile/',
        ProfileDashboardView.as_view(),
        name='profile_dashboard'
    ),
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    )
]
