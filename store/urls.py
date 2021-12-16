from django.urls import path
from .views import (
    homepage_view,
    cart_view,
    checkout_view,
    product_view,
)

app_name = 'store'

urlpatterns = [
    path('', homepage_view, name="homepage"),
    path('cart', cart_view, name="cart-page"),
    path('checkout', checkout_view, name="checkout-page"),
    path('product/<int:product_id>', product_view, name="product-page"),
]
