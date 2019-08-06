from django.urls import path

from .views import (
        ProductListView,
        ProductDetailSlugView,
        ProductDownloadView
        )

app_name = 'products'
urlpatterns = [
    # url(r'^$', ProductListView.as_view(), name='list'),
    # url(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),
    # url(r'^(?P<slug>[\w-]+)/(?P<pk>\d+)/$', ProductDownloadView.as_view(), name='download'),
    path('', ProductListView.as_view(), name='products'),
    path('<slug:slug>/', ProductDetailSlugView.as_view(), name='detail'),
    path('<slug:slug>/<str:pk>/', ProductDownloadView.as_view(), name='download')
]
