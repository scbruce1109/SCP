from django.urls import path

from .views import (
        cart_home,
        cart_update,
        checkout_home,
        checkout_done_view,
        paypal_transaction_complete_view,
        discount_code_apply_view,
        )

app_name = 'carts'
urlpatterns = [
    path('', cart_home, name='home'),
    path('checkout/', checkout_home, name='checkout'),
    path('checkout/success', checkout_done_view, name='success'),
    path('update/', cart_update, name='update'),
    path('paypal-transaction-complete/', paypal_transaction_complete_view, name='paypal-endpoint'),
    path('apply-discount/', discount_code_apply_view, name='apply-discount'),
]
