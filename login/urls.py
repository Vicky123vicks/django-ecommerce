# login/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'), # for /login/
    path('ecommerce/', views.ecommerce_view, name='ecommerce'),
    path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.cart_view, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),  # ✅ ADD THIS LINE
    path('register/', views.register_view, name='register')
]




