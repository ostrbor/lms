from auction.models import Auction, Bid
from rest_framework import serializers


class AuctionListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Auction
        fields = ('id', 'title', 'current_price', 'price_step', 'close_at',
                  'owner')


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ('id', 'price', 'auction')


class AuctionDetailSerializer(AuctionListSerializer):
    bids = BidSerializer(source='bid_set', many=True)

    class Meta(AuctionListSerializer.Meta):
        fields = AuctionListSerializer.Meta.fields + ('bids', )
