from auction.models import Auction
from auction.models import User
from auction.serializers import (AuctionListSerializer, BidCreateSerializer,
                                 AuctionDetailSerializer, UserCreateSerializer,
                                 AuctionCreateSerializer)
from rest_framework import generics
from rest_framework.permissions import AllowAny


class UserCreate(generics.CreateAPIView):
    """
    post: Create user
    """
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny, )

    def perform_create(self, serializer):
        User.objects.create_user(**serializer.validated_data)


class AuctionListCreate(generics.ListCreateAPIView):
    """
    get: List auctions
    post: Create auction
    """
    queryset = Auction.objects.all()
    filter_fields = ('is_opened', )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AuctionListSerializer
        else:
            return AuctionCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AuctionDetail(generics.RetrieveAPIView):
    """
    get: Auction details
    """
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer


class BidCreate(generics.CreateAPIView):
    """
    get: Create bid
    """
    serializer_class = BidCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
