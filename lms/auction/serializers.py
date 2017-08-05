from auction.models import Auction, Bid
from rest_framework import serializers


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ('id', 'title', 'current_price', 'price_step', 'close_at')


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ('id', 'price', 'auction', 'user')
