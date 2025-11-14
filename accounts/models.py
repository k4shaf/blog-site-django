from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class UserProfile(models.Model):
    """Extended user profile model"""
    ROLE_CHOICES = [
        ('reader', 'Reader'),
        ('author', 'Author'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='reader'
    )
    bio = models.TextField(blank=True, help_text="User biography")
    avatar = models.ImageField(
        upload_to='avatars/%Y/%m/%d/',
        null=True,
        blank=True
    )
    website = models.URLField(blank=True)
    is_email_verified = models.BooleanField(default=False)
    author_request_pending = models.BooleanField(default=False, help_text="User has requested author role")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    def is_admin(self):
        return self.role == 'admin'

    def is_author(self):
        return self.role in ['author', 'admin']

    def is_reader(self):
        return True  # All users are at least readers
