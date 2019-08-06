from django.urls import path

from .views import (
        BeatListView,
        BeatDetailSlugView,
        # ProductDownloadView
        )

app_name = 'beatstore'
urlpatterns = [
    # url(r'^$', ProductListView.as_view(), name='list'),
    # url(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),
    # url(r'^(?P<slug>[\w-]+)/(?P<pk>\d+)/$', ProductDownloadView.as_view(), name='download'),
    path('', BeatListView.as_view(), name='beatstore'),
    path('<str:slug>/', BeatDetailSlugView.as_view(), name='detail')
]
