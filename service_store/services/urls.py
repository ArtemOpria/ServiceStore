from django.urls import path
from . import views


urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('search/', views.search_services, name='search_services'),
    path('<int:service_id>/', views.service_detail, name='service_detail'),
    path('toggle-favorite/<int:service_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorites, name='favorites'),
    path('check_auth_for_cart/<int:service_id>/', views.check_auth_for_cart, name='check_auth_for_cart'),
]
