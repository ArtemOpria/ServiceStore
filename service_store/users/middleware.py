from django.urls import resolve
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class RoleMiddleware:
    """
    Middleware to enforce role-based access control for admin URLs.
    
    This middleware checks if a user is trying to access admin pages and verifies
    if they have the appropriate role to do so.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_url = resolve(request.path_info)
            
            if 'admin' in request.path and current_url.app_name == 'admin':
                if request.user.role != 'admin' and not request.user.is_superuser:
                    messages.error(request, _('You do not have permission to access the admin area.'))
                    return redirect('home')
            
            if 'manager' in request.path and current_url.app_name == 'manager':
                if request.user.role != 'manager' and not request.user.is_superuser:
                    messages.error(request, _('You do not have permission to access the manager area.'))
                    return redirect('home')
        
        response = self.get_response(request)
        return response
