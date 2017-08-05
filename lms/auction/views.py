from auction.models import Auction, Bid
from auction.serializers import AuctionSerializer, BidSerializer
from rest_framework import generics


class AuctionList(generics.ListCreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer


class AuctionDetail(generics.RetrieveAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer


class BidCreate(generics.CreateAPIView):
    serializer_class = BidSerializer
