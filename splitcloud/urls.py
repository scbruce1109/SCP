"""splitcloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

from .views import home_page, new_home, BeatStoreView, about_page, services_page, contact_page
# from accounts.views import LoginView, RegisterView, GuestRegisterView
# from addresses.views import checkout_address_create_view, checkout_address_reuse_view
# from analytics.views import SalesView, SalesAjaxView
# from billing.views import payment_method_view, payment_method_create_view, paypal_transaction_complete_view
# from carts.views import cart_detail_api_view
# from marketing.views import MarketingPreferenceUpdateView, MailchimpWebhookView, SubscribeArtistView
# from orders.views import LibraryView
from django.conf.urls import url
# from beatstore.views import BeatListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    # path('new/', new_home, name='new-home'),
    # path('about/', about_page, name='about'),
    # path('services/', services_page, name='services'),
    # path('contact/', contact_page, name='contact'),
    # path('beatstore/', BeatStoreView.as_view(), name='beatstore'),
    # path('subscribe/', SubscribeArtistView.as_view(), name='subscribe'),
    # path('account/', include(("accounts.urls", 'accounts'), namespace='account')),
    # path('accounts/', include("accounts.passwords.urls")),
    # path('analytics/sales/', SalesView.as_view(), name='sales-analytics'),
    # path('analytics/sales/data/', SalesAjaxView.as_view(), name='sales-analytics-data'),
    # path('api/cart/', cart_detail_api_view, name='api-cart'),
    # path('cart/', include(("carts.urls", 'carts'), namespace='cart')),
    # path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('library/', LibraryView.as_view(), name='library'),
    # path('register/', RegisterView.as_view(), name='register'),
    # path('products/', include(("products.urls", 'products'), namespace='products')),
    # path('search/', include(("search.urls", 'search'), namespace='search')),
    # path('orders/', include(("orders.urls", 'orders'), namespace='orders')),
    # path('checkout/address/create/', checkout_address_create_view, name='checkout_address_create'),
    # path('checkout/address/reuse/', checkout_address_reuse_view, name='checkout_address_reuse'),
    # path('billing/payment-method/', payment_method_view, name='billing-payment-method'),
    # path('billing/payment-method/create/', payment_method_create_view, name='billing-payment-method-endpoint'),
    # path('billing/paypal-transaction-complete/', paypal_transaction_complete_view, name='paypal-endpoint'),
    # path('register/guest/', GuestRegisterView.as_view(), name='guest_register'),
    # path('settings/email/', MarketingPreferenceUpdateView.as_view(), name='marketing-pref'),
    # path('webhooks/mailchimp/', MailchimpWebhookView.as_view(), name='webhooks-mailchimp'),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
