from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser
from .models.utils import UserStatus


class CustomUserAdmin(UserAdmin):

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = (
        'email',
        'display_name',
        'is_staff',
        'is_active',
        'is_verified'
    )
    list_filter = (
        'email',
        'is_staff',
        'is_active',
        'is_verified'
    )
    fieldsets = (
        (
            None, {
                'fields': (
                    'email',
                    'password'
                )
            }
        ),
        (
            'Permissions', {
                'fields': (
                    'is_staff',
                    'is_active',
                    'is_verified',
                    'groups',
                    'user_permissions'
                )
            }
        ),
    )
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': (
                    'display_name',
                    'email',
                    'password1',
                    'password2',
                    'is_staff',
                    'is_active',
                    'groups',
                    'user_permissions'
                )
            }
        ),
    )
    search_fields = (
        'email',
        'display_name'
    )
    ordering = (
        'email',
    )

    @admin.display(description='Current Status')
    def current_status(self, obj: CustomUser):
        """
        Display the current status of the client user.
        """
        STATUSES_MAPPING = {
            UserStatus.ACTIVE: (
                '<span style="color: green;">'
                f'{UserStatus.ACTIVE.label}</span>'
            ),
            UserStatus.PENDING: (
                '<span style="color: orange;">'
                f'{UserStatus.PENDING.label}</span>'
            ),
            UserStatus.SUSPENDED: (
                '<span style="color: red;">'
                f'{UserStatus.SUSPENDED.label}</span>'
            ),
            UserStatus.UNKNOWN: (
                '<span style="color: grey;">'
                f'{UserStatus.UNKNOWN.label}</span>'
            )
        }

        return format_html(STATUSES_MAPPING[obj.status])


# Register the subclassed custom user admin.
admin.site.register(CustomUser, CustomUserAdmin)
