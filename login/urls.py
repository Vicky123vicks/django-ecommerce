from django.urls import path
from .views import login_view, ecommerce_view, logout_view, add_to_cart, cart_view, product_detail_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('ecommerce/', ecommerce_view, name='ecommerce'),
    path('logout/', logout_view, name='logout'),
    path('product/<int:product_id>/', product_detail_view, name='product_detail'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart'),
]

