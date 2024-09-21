from django.contrib import admin

from .models import Admin as AdminProfile
from .models import Client


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the `Admin` model.
    """
    # Fields to display in the admin list view
    list_display = (
        'admin_number',
        'user',
        'full_name',
        'department',
        'is_active',
        'is_verified',
        'created_at'
    )

    # Fields that can be clicked to navigate to the detail page.
    list_display_links = ('admin_number',)

    # Filters for filtering admins.
    list_filter = (
        'is_active',
        'is_verified',
        'department'
    )

    # Searchable fields in the admin panel.
    search_fields = (
        'user__username',
        'admin_number',
        'first_name',
        'last_name',
        'department'
    )

    # Fields that are read-only.
    readonly_fields = ('admin_number', 'user', 'created_at', 'modified_at')

    # Fieldsets for organizing the fields in the detail page.
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'user',
                'admin_number',
                'first_name',
                'last_name',
                'department',
                'avatar'
            )
        }),
        ('Status', {
            'fields': (
                'is_active',
                'is_verified'
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'modified_at'
            ),
        }),
    )

    # Ordering of admins.
    ordering = ('-created_at',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the `Client` model.
    """
    # Fields to display in the admin list view.
    list_display = (
        'display_name',
        'user',
        'mobile_number',
        'is_active',
        'is_verified',
        'created_at'
    )

    # Fields that can be clicked to navigate to the detail page.
    list_display_links = ('display_name',)

    # Filters for filtering clients.
    list_filter = (
        'is_active',
        'is_verified',
        'is_sms_verified'
    )

    # Searchable fields in the admin panel.
    search_fields = (
        'user__username',
        'display_name',
        'mobile_number'
    )

    # Fields that are read-only.
    readonly_fields = ('created_at', 'modified_at')

    # Fieldsets for organizing the fields in the detail page.
    fieldsets = (
        (
            'Basic Information', {
                'fields': (
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
                    'is_sms_verified'
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
