from django.contrib import admin, messages
from django.utils.html import format_html

from .models import Shop, ShopFollower


class ShopFollowerInline(admin.TabularInline):
    """
    Inline admin interface for ShopFollower model within Shop admin.
    """
    model = ShopFollower
    fk_name = 'fk_shop'
    extra = 0  # No extra blank forms
    readonly_fields = (
        'fk_client',
        'date_followed'
    )
    can_delete = True  # Allow deletion of followers
    verbose_name = 'Follower'
    verbose_name_plural = 'Followers'
    search_fields = (
        'fk_client__user__username',
        'fk_client__display_name'
    )
    list_display = (
        'fk_client_display',
        'date_followed'
    )

    def fk_client_display(self, obj):
        """
        Display the client's display name.
        """
        return obj.fk_client.display_name
    fk_client_display.short_description = 'Client'


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the `Shop` model.
    """
    list_display = (
        'shop_id',
        'owner',
        'follower_count',
        'created_at',
        'modified_at',
        'verification_status',
        'view_legal_id',
        'view_verification_documents'
    )

    list_filter = (
        'is_active',
        'created_at',
        'modified_at',
        'owner__user__username'
    )

    search_fields = (
        'owner__user__username',
        'owner__display_name',
        'description'
    )

    readonly_fields = (
        'shop_id',
        'follower_count',
        'created_at',
        'modified_at',
        'verification_status'
    )

    fieldsets = (
        (
            'Shop Details', {
                'fields': (
                    'shop_id',
                    'owner',
                    'description',
                    'follower_count'
                )
            }
        ),
        (
            'Verification Details', {
                'fields': (
                    'legal_id',
                    'verification_document',
                    'verification_status'
                )
            }
        ),
        (
            'Timestamps', {
                'fields': (
                    'created_at',
                    'modified_at',
                )
            }
        ),
    )

    inlines = [ShopFollowerInline]

    list_per_page = 25  # Number of shops to display per page

    actions = ['approve_shops', 'reject_shops']

    def description_truncated(self, obj: Shop):
        """
        Truncate the description for better display in list view.
        """
        if obj.description:
            return (
                obj.description[:75] + '...'
            ) if len(obj.description) > 75 else obj.description
        return ''

    description_truncated.short_description = 'Description'

    def verification_status(self, obj: Shop):
        """
        Display the verification status with color coding.
        """
        if obj.is_active:
            return format_html(
                '<span style="color: green;">Verified</span>'
            )
        elif obj.verification_document:
            return format_html(
                '<span style="color: orange;">Pending Verification</span>'
            )
        else:
            return format_html(
                '<span style="color: red;">Unverified</span>'
            )

    verification_status.short_description = 'Verification Status'
    verification_status.admin_order_field = 'is_active'

    def view_legal_id(self, obj: Shop):
        """
        Provide a link to view the uploaded legal ID.
        """
        if obj.legal_id:
            legal_id_url = obj.legal_id.url
            return format_html(
                '<a href="{}" target="_blank">View ID</a>',
                legal_id_url
            )
        return format_html('<span style="color: red;">No Legal ID</span>')

    view_legal_id.short_description = 'Legal ID'

    def view_verification_documents(self, obj: Shop):
        """
        Provide links to view the uploaded verification documents.
        """
        if obj.verification_document:
            verification_doc_url = obj.verification_document.url
            return format_html(
                '<a href="{}" target="_blank">View Document</a>',
                verification_doc_url
            )
        return format_html('<span style="color: red;">No Document</span>')

    view_verification_documents.short_description = 'Verification Document'

    @admin.action(description='Approve a shop after verifying documents.')
    def approve_shops(self, request, queryset):
        """
        Admin action to approve selected shops.
        """
        updated = queryset.filter(is_active=False).update(
            is_active=True
        )
        self.message_user(
            request,
            f'{updated} shop(s) successfully approved.',
            messages.SUCCESS
        )

    approve_shops.short_description = 'Approve selected shops'

    @admin.action(description='Remove the approved shop status.')
    def reject_shops(self, request, queryset):
        """
        Admin action to reject selected shops by deactivating them.
        Optionally, you can prompt for reasons or handle document removal.
        """
        updated = queryset.filter(is_active=True).update(is_active=False)
        self.message_user(
            request,
            f'{updated} shop(s) successfully rejected/deactivated.',
            messages.WARNING
        )

    reject_shops.short_description = 'Reject selected shops'


@admin.register(ShopFollower)
class ShopFollowerAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the `ShopFollower` model.
    """
    list_display = (
        'fk_client_display',
        'fk_shop_display',
        'date_followed'
    )

    list_display_links = (
        'fk_client_display',
        'fk_shop_display'
    )

    list_filter = (
        'fk_shop',
        'date_followed'
    )

    search_fields = (
        'fk_client__user__username',
        'fk_client__display_name',
        'fk_shop__name'
    )

    ordering = ('-date_followed',)

    list_per_page = 25

    def fk_shop_display(self, obj: ShopFollower):
        """
        Display the shop's name.
        """
        return obj.fk_shop.shop_id

    fk_shop_display.short_description = 'Shop'

    def fk_client_display(self, obj: ShopFollower):
        """
        Display the client's display name.
        """
        return obj.fk_client.display_name

    fk_client_display.short_description = 'Client'
