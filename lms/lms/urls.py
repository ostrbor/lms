from django.conf.urls import url, include
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title='Auction API')

# TODO: login urlpatterns for debugging
urlpatterns = [
    url(r'^schema/$', schema_view),
    url(r'^api/v1/', include(
        'rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/', include('auction.urls')),
]
