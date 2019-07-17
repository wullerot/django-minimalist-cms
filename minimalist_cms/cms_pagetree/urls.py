from __future__ import unicode_literals

from django.conf.urls import url

from .views import PageDetailView


SLUG_REGEXP = '[0-9A-Za-z-_.//]+'


urlpatterns = [
    url(
        r'^$',
        PageDetailView.as_view(),
        name='page-detail-home',
    ),
    url(
        r'^(?P<slug>[0-9A-Za-z-_.//]+)/$',
        PageDetailView.as_view(),
        name='page-detail',
    ),
]
