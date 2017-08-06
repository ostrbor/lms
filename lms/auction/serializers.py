from datetime import datetime
import pytz
from auction.models import Auction, Bid, User
from rest_framework import serializers
from rest_framework.serializers import ValidationError


class AuctionListSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    winner = serializers.ReadOnlyField(source='winner.username')

    class Meta:
        model = Auction
        fields = '__all__'
        extra_kwargs = {'url': {'view_name': 'auction_detail'}}


class AuctionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ('id', 'item_description', 'initial_price', 'price_step',
                  'close_at')

    def validate_close_at(self, value):
        now = datetime.now(pytz.utc)
        if value <= now:
            raise ValidationError('Close date is in the past.')


class BidDetailNestedSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Bid
        fields = ('id', 'price', 'username')


class AuctionDetailSerializer(serializers.ModelSerializer):
    bids = BidDetailNestedSerializer(many=True)

    class Meta:
        model = Auction
        fields = ('id', 'item_description', 'initial_price', 'current_price',
                  'price_step', 'close_at', 'owner', 'bids', 'is_opened')


class BidCreateSerializer(serializers.ModelSerializer):
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
            msg = f'Bid price must be greater than current price '\
                f'{current_price}'
            raise ValidationError(msg)
        if (data['price'] - current_price) % price_step != 0:
            msg = f'Bid price = {current_price} + k*{price_step}'
            raise ValidationError(msg)
        return data


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
