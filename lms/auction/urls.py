from django.conf.urls import url
from .views import AuctionList, AuctionDetail, BidCreate, UserCreate
from rest_framework.authtoken import views

urlpatterns = [
    url(r'^users/$', UserCreate.as_view(), name='create_user'),
    url(r'^tokens/', views.obtain_auth_token, name='get_token'),
    url(r'^auctions/$', AuctionList.as_view(), name='auction_list'),
    url(r'^auctions/(?P<pk>[0-9]+)/$',
        AuctionDetail.as_view(),
        name='auction_detail'),
    url(r'^auctions/(?P<pk>[0-9]+)/bids$',
        BidCreate.as_view(),
        name='create_bid'),
]
