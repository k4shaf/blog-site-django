from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Post
from accounts.models import UserProfile


@receiver(post_save, sender=Post)
def post_published_signal(sender, instance, created, **kwargs):
    """Send notification when a post is published"""
    if instance.status == 'published' and instance.published_at:
        # Send email to admin
        subject = f"New Post Published: {instance.title}"
        html_message = render_to_string('blog/emails/post_published.html', {
            'post': instance,
            'author': instance.author,
        })
        
        # Send to admin
        admin_email = settings.DEFAULT_FROM_EMAIL
        try:
            send_mail(
                subject,
                f"New post published: {instance.title}",
                settings.DEFAULT_FROM_EMAIL,
                [admin_email],
                html_message=html_message,
                fail_silently=True,
            )
        except Exception as e:
            print(f"Error sending email: {e}")


@receiver(post_save, sender=UserProfile)
def create_default_permissions(sender, instance, created, **kwargs):
    """Create default permissions for new users"""
    if created:
        # Additional setup for new user profiles can be added here
        pass


# Import signals when app is ready
def ready():
    import blog.signals
