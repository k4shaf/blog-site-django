from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin for UserProfile model"""
    list_display = ('user', 'role_badge', 'author_request_status', 'is_email_verified', 'created_at')
    list_filter = ('role', 'author_request_pending', 'is_email_verified', 'created_at')
    search_fields = ('user__username', 'user__email', 'bio')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'role')
        }),
        ('Profile Details', {
            'fields': ('bio', 'avatar', 'website')
        }),
        ('Author Request', {
            'fields': ('author_request_pending',),
            'description': 'Users can request to become authors to publish posts.'
        }),
        ('Account Status', {
            'fields': ('is_email_verified',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['approve_author_requests', 'reject_author_requests']
    ordering = ('-created_at',)

    def role_badge(self, obj):
        colors = {
            'admin': 'red',
            'author': 'blue',
            'reader': 'green'
        }
        color = colors.get(obj.role, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_role_display()
        )
    role_badge.short_description = 'Role'

    def author_request_status(self, obj):
        if obj.author_request_pending:
            return format_html(
                '<span style="background-color: orange; color: white; padding: 3px 8px; border-radius: 3px;">⏳ Pending</span>'
            )
        elif obj.is_author():
            return format_html(
                '<span style="background-color: green; color: white; padding: 3px 8px; border-radius: 3px;">✓ Author</span>'
            )
        return '—'
    author_request_status.short_description = 'Author Status'

    def approve_author_requests(self, request, queryset):
        """Bulk action to approve author role requests"""
        updated = 0
        for profile in queryset.filter(author_request_pending=True):
            if profile.role == 'reader':  # Only upgrade readers
                profile.role = 'author'
                profile.author_request_pending = False
                profile.save()
                updated += 1
        
        if updated > 0:
            self.message_user(request, f'✓ Approved {updated} author role request(s).')
        else:
            self.message_user(request, 'No pending requests to approve.', level='warning')
    approve_author_requests.short_description = '✓ Approve author role requests'

    def reject_author_requests(self, request, queryset):
        """Bulk action to reject author role requests"""
        updated = queryset.filter(author_request_pending=True).update(author_request_pending=False)
        if updated > 0:
            self.message_user(request, f'✗ Rejected {updated} author role request(s).')
        else:
            self.message_user(request, 'No pending requests to reject.', level='warning')
    reject_author_requests.short_description = '✗ Reject author role requests'

