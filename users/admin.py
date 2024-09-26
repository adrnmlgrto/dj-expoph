from django.contrib import admin
from django.utils.html import format_html

from .models import Admin as AdminProfile
from .models import Client
from .models.utils import UserStatus


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the `Admin` model.
    """
    # Fields to display in the admin list view
    list_display = (
        'admin_number',
        'display_name',
        'department',
        'current_status',
        'created_at',
        'modified_at'
    )

    # Filters for filtering admins.
    list_filter = (
        'is_active',
        'is_verified',
        'department'
    )

    # Searchable fields in the admin panel.
    search_fields = (
        'admin_number',
        'user__username',
        'first_name',
        'last_name',
        'department'
    )

    # Fields that are read-only.
    readonly_fields = (
        'admin_number',
        'user',
        'created_at',
        'modified_at',
        'current_status'
    )

    # Fieldsets for organizing the fields in the detail page.
    fieldsets = (
        (
            'Basic Information', {
                'fields': (
                    'admin_number',
                    'user',
                    'first_name',
                    'last_name',
                    'department',
                    'avatar'
                )
            }
        ),
        (
            'Status', {
                'fields': (
                    'is_active',
                    'is_verified',
                    'current_status'
                )
            }
        ),
        (
            'Timestamps', {
                'fields': (
                    'created_at',
                    'modified_at'
                ),
            }
        ),
    )

    # Ordering of admins.
    ordering = ('-created_at',)

    @admin.display(description='Current Status')
    def current_status(self, obj: AdminProfile):
        """
        Display the current status of the admin user.
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


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the `Client` model.
    """
    # Fields to display in the admin list view.
    list_display = (
        'client_number',
        'client_user',
        'mobile_number',
        'current_status',
        'created_at',
        'modified_at'
    )

    # Filters for filtering clients.
    list_filter = (
        'is_active',
        'is_verified',
        'is_sms_verified'
    )

    # Searchable fields in the admin panel.
    search_fields = (
        'client_number',
        'user__username',
        'display_name',
        'mobile_number'
    )

    # Fields that are read-only.
    readonly_fields = (
        'client_number',
        'created_at',
        'modified_at',
        'current_status'
    )

    # Fieldsets for organizing the fields in the detail page.
    fieldsets = (
        (
            'Basic Information', {
                'fields': (
                    'client_number',
                    'user',
                    'avatar',
                    'display_name',
                    'mobile_number',
                    'shipping_address'
                )
            }
        ),
        (
            'Status', {
                'fields': (
                    'is_active',
                    'is_verified',
                    'is_sms_verified',
                    'current_status'
                )
            }
        ),
        (
            'Subscriptions', {
                'fields': (
                    'newsletter',
                )
            }
        ),
        (
            'Timestamps', {
                'fields': (
                    'created_at',
                    'modified_at'
                )
            }
        ),
    )

    # Ordering of clients.
    ordering = ('-created_at',)

    @admin.display(description='Client User')
    def client_user(self, obj: Client):
        """
        Display both the display name and username of the
        client user on the admin dashboard.
        """
        return f'{obj.display_name} ({obj.user.username})'

    @admin.display(description='Current Status')
    def current_status(self, obj: Client):
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
