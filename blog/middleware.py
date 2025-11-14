from django.utils.deprecation import MiddlewareMixin
from .models import UserActivity


class UserActivityMiddleware(MiddlewareMixin):
    """Middleware to track user activity"""
    
    def process_request(self, request):
        # Track login/logout events are handled in views
        # This middleware can be extended for additional tracking
        return None

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
