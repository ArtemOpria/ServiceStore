from django.urls import path
from . import views
from . import views_ajax


urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_cart/', views_ajax.update_cart, name='update_cart'),
]
