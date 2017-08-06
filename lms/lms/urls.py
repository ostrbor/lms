from django.conf.urls import url, include

# TODO: comment first urlpattern (use for debugging)
urlpatterns = [
    url(r'^api/v1/', include(
        'rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/', include('auction.urls')),
]
