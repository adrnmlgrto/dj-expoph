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
        'current_status',
        'created_at',
        'modified_at'
    )
    list_filter = (
        'email',
        'is_staff',
        'is_active',
        'is_verified'
    )
    fieldsets = (
        (
            'User Details', {
                'fields': (
                    'email',
                    'password',
                    'avatar'
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
        STATUS_COLOR_MAPPING = {
            UserStatus.ACTIVE: 'green',
            UserStatus.PENDING: 'orange',
            UserStatus.SUSPENDED: 'red',
            UserStatus.UNKNOWN: 'grey',
        }
        color = STATUS_COLOR_MAPPING[obj.status]
        return format_html(
            f'<span style="color: {color};">{obj.status.label}</span>'
        )


# Register the subclassed custom user admin.
admin.site.register(CustomUser, CustomUserAdmin)
