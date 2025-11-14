from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Tag, Post, Comment, UserActivity


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin for Category model"""
    list_display = ('name', 'slug', 'post_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-created_at',)

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Number of Posts'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin for Tag model"""
    list_display = ('name', 'slug', 'post_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-created_at',)

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Number of Posts'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin for Post model"""
    list_display = ('title', 'author', 'category', 'status_badge', 'views_count', 'published_at')
    list_filter = ('status', 'category', 'created_at', 'published_at')
    search_fields = ('title', 'slug', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views_count', 'created_at', 'updated_at', 'published_at')
    filter_horizontal = ('tags',)
    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'featured_image')
        }),
        ('Meta', {
            'fields': ('tags',)
        }),
        ('Status & Dates', {
            'fields': ('status', 'views_count', 'created_at', 'updated_at', 'published_at')
        }),
    )
    ordering = ('-published_at', '-created_at')

    def status_badge(self, obj):
        color = 'green' if obj.status == 'published' else 'orange'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin for Comment model"""
    list_display = ('user', 'post', 'status_badge', 'created_at')
    list_filter = ('status', 'created_at', 'post')
    search_fields = ('content', 'user__username', 'post__title')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['approve_comments', 'reject_comments']
    ordering = ('-created_at',)

    def status_badge(self, obj):
        colors = {
            'approved': 'green',
            'pending': 'orange',
            'rejected': 'red'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def approve_comments(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} comment(s) approved.')
    approve_comments.short_description = 'Approve selected comments'

    def reject_comments(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} comment(s) rejected.')
    reject_comments.short_description = 'Reject selected comments'


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """Admin for UserActivity model"""
    list_display = ('user', 'activity_type', 'post', 'ip_address', 'created_at')
    list_filter = ('activity_type', 'created_at', 'user')
    search_fields = ('user__username', 'post__title', 'ip_address')
    readonly_fields = ('user', 'activity_type', 'post', 'ip_address', 'user_agent', 'created_at')
    ordering = ('-created_at',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
