from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import AdminSite
from .models import CustomUser, Profile
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from services.models import Review


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    inlines = (ProfileInline,)
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (_('Дані для входу'), {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Роль'), {'fields': ('role',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


class AdminSiteForAdmins(AdminSite):
    site_header = _('Administrator Portal')
    site_title = _('Administrator Portal')
    index_title = _('User Management')

class AdminSiteForManagers(AdminSite):
    site_header = _('Manager Portal')
    site_title = _('Manager Portal')
    index_title = _('Service Management')

admin_site = AdminSiteForAdmins(name='admin_site')
manager_site = AdminSiteForManagers(name='manager_site')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__email', 'service__name', 'comment')
    readonly_fields = ('created_at',)
    fieldsets = (
        (_('Інформація про відгук'), {'fields': ('user', 'service')}),
        (_('Деталі відгуку'), {'fields': ('rating', 'comment')}),
        (_('Дата створення'), {'fields': ('created_at',)}),
    )

admin.site.unregister(Group)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Review, ReviewAdmin)
admin_site.register(CustomUser, CustomUserAdmin)
admin_site.register(Review, ReviewAdmin)
manager_site.register(Review, ReviewAdmin)
