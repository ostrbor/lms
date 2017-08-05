from auction.models import Auction, Bid
from auction.serializers import (AuctionListSerializer, BidSerializer,
                                 AuctionDetailSerializer,
                                 AuctionBaseSerializer)
from rest_framework import generics


class AuctionList(generics.ListCreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionListSerializer
    filter_fields = ('is_opened', )

    list_serializer = AuctionListSerializer
    create_serializer = AuctionBaseSerializer

    def list(self, *args, **kwargs):
        self.serializer_class = self.list_serializer
        return super().list(*args, **kwargs)

    def create(self, *args, **kwargs):
        self.serializer_class = self.create_serializer
        return super().create(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AuctionDetail(generics.RetrieveAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer


class BidCreate(generics.CreateAPIView):
    serializer_class = BidSerializer
