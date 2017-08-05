from auction.models import Auction, Bid
from rest_framework import serializers


class AuctionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ('id', 'title', 'owner', 'current_price', 'price_step',
                  'close_at')


class AuctionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ('id', 'title', 'current_price', 'price_step', 'close_at')


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ('id', 'price', 'auction', 'user')


class AuctionDetailSerializer(AuctionListSerializer):
    bids = BidSerializer(source='bid_set', many=True)

    class Meta(AuctionListSerializer.Meta):
        fields = AuctionListSerializer.Meta.fields + ('bids', )
