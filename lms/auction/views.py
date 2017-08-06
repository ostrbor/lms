from auction.models import Auction
from auction.models import User
from auction.serializers import (AuctionListSerializer, BidSerializer,
                                 AuctionDetailSerializer, UserSerializer)
from rest_framework import generics
from rest_framework.permissions import AllowAny


class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

    def perform_create(self, serializer):
        User.objects.create_user(**serializer.validated_data)


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
