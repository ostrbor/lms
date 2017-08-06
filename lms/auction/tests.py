from django.test import TestCase
from unittest.mock import patch
from auction.models import Auction, User, Bid
from datetime import datetime


class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='User', password='123', email='user@gmail.com')
        close_at = datetime.now()
        self.auction = Auction(
            title='title',
            current_price=10,
            price_step=1,
            close_at=close_at,
            owner=self.user)

    @patch('django.db.models.signals.post_save.send')
    def test_auction_signal_triggered(self, mock):
        # WARNING: check for all post_save signals
        # New auction is created
        self.auction.save()
        self.assertTrue(mock.called)
        # New bid is made
        self.auction.current_price = 11
        self.auction.save()
        self.assertEqual(mock.call_count, 2)

    def test_bid_save_updates_auction_price(self):
        self.auction.save()
        bid = Bid(price=11, auction=self.auction, user=self.user)
        bid.save()
        self.auction.refresh_from_db()
        self.assertEqual(self.auction.current_price, bid.price)
