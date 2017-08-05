from auction.models import Auction, Bid
from auction.serializers import (AuctionListSerializer, BidSerializer,
                                 AuctionDetailSerializer)
from rest_framework import generics


class AuctionList(generics.ListCreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionListSerializer
    filter_fields = ('is_opened', )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AuctionDetail(generics.RetrieveAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer


class BidCreate(generics.CreateAPIView):
    serializer_class = BidSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
