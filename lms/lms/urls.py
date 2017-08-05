from django.conf.urls import url, include
from auction.views import AuctionList, AuctionDetail, BidCreate, UserCreate
from rest_framework.authtoken import views

# TODO: comment first urlpattern (use for debugging)
urlpatterns = [
    url(r'^', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^user/$', UserCreate.as_view(), name='user'),
    url(r'^token/', views.obtain_auth_token, name='token'),
    url(r'^auctions/$', AuctionList.as_view(), name='auction-list'),
    url(r'^auctions/(?P<pk>[0-9]+)/$',
        AuctionDetail.as_view(),
        name='auction-detail'),
    url(r'^auctions/(?P<pk>[0-9]+)/bids$', BidCreate.as_view(), name='bid'),
]
