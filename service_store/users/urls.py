from django.urls import path
from . import views
from .admin import admin_site, manager_site


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/password_change', views.password_change, name='password_change'),
    path('admin/', admin_site.urls, name='admin_site'),  # For administrators (user management)
    path('manager/', manager_site.urls, name='manager_site'),  # For managers (service management)
]
