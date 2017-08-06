from datetime import datetime
import pytz
from auction.models import Auction, Bid, User
from rest_framework import serializers
from rest_framework.serializers import ValidationError


class AuctionListSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Auction
        fields = ('url', 'id', 'item_description', 'initial_price',
                  'price_step', 'close_at', 'owner')
        extra_kwargs = {'url': {'view_name': 'auction_detail'}}

    def validate_close_at(self, value):
        now = datetime.now(pytz.utc)
        if value <= now:
            raise ValidationError('Close date is in the past.')


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ('id', 'price', 'auction')

    def validate(self, data):
        auction = data['auction']
        if not auction.is_opened:
            raise ValidationError('Auction is closed.')
        bid_user = self.context['request'].user
        if bid_user == auction.owner:
            raise ValidationError('Owner of auction can not bid.')
        current_price = auction.current_price
        price_step = auction.price_step
        if data['price'] <= current_price:
            msg = 'Bid price is lower or equal to auction current price.'
            raise ValidationError(msg)
        if (data['price'] - current_price) % price_step != 0:
            msg = 'The remainder of division of bid price and auction price '\
                'step is not equal to zero.'
            raise ValidationError(msg)
        return data


class AuctionDetailSerializer(AuctionListSerializer):
    class Meta(AuctionListSerializer.Meta):
        fields = AuctionListSerializer.Meta.fields + ('bids', 'current_price')


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
