from auction.models import Auction, Bid, User
from rest_framework import serializers
from rest_framework.serializers import ValidationError


class AuctionListSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Auction
        fields = ('url', 'id', 'item_description', 'initial_price',
                  'current_price', 'price_step', 'close_at', 'owner')


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
    bids = BidSerializer(source='bid_set', many=True)

    class Meta(AuctionListSerializer.Meta):
        fields = AuctionListSerializer.Meta.fields + ('bids', )


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
