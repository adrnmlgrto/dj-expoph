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
        STATUSES_MAPPING = {
            UserStatus.ACTIVE.label: (
                'green', UserStatus.ACTIVE.label
            ),
            UserStatus.PENDING.label: (
                'orange', UserStatus.PENDING.label
            ),
            UserStatus.SUSPENDED.label: (
                'red', UserStatus.SUSPENDED.label
            ),
            UserStatus.UNKNOWN.label: (
                'grey', UserStatus.UNKNOWN.label
            ),
        }

        color, label = STATUSES_MAPPING[obj.status]
        return format_html(
            f'<span style="color: {color};">{label}</span>'
        )


# Register the subclassed custom user admin.
admin.site.register(CustomUser, CustomUserAdmin)
