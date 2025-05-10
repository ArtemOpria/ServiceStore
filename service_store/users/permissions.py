from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class RoleRequiredMixin(UserPassesTestMixin):
    """
    Mixin to restrict view access based on user role.
    """
    required_role = None  # Should be set to 'admin' or 'manager'
    permission_denied_message = _('You do not have permission to access this page.')
    login_url = reverse_lazy('login')
    
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        
        # If no specific role is required, just check if user is authenticated
        if self.required_role is None:
            return True
            
        # Check if user has the required role
        return self.request.user.role == self.required_role
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(self.login_url)
        raise PermissionDenied(self.permission_denied_message)


class AdminRequiredMixin(RoleRequiredMixin):
    """
    Mixin to restrict view access to administrators only.
    """
    required_role = 'admin'
    permission_denied_message = _('Only administrators can access this page.')


class ManagerRequiredMixin(RoleRequiredMixin):
    """
    Mixin to restrict view access to managers only.
    """
    required_role = 'manager'
    permission_denied_message = _('Only managers can access this page.')