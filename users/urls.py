from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import CustomLoginView, ProfileDashboardView, RegisterView

app_name = 'users'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileDashboardView.as_view(), name='profile')
]
