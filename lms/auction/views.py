from auction.models import Auction, Bid
from auction.serializers import (AuctionListSerializer, BidSerializer,
                                 AuctionDetailSerializer)
from rest_framework import generics


class AuctionList(generics.ListCreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionListSerializer


class AuctionDetail(generics.RetrieveAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer


class BidCreate(generics.CreateAPIView):
    serializer_class = BidSerializer
