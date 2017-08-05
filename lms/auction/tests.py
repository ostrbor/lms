from django.test import TestCase
from unittest.mock import patch
from auction.models import Auction, User
from datetime import datetime


class SignalsTestCase(TestCase):
    @patch('auction.signals.auction.send')
    def test_auction_signal_triggered(self, mock):
        owner = User.objects.get(pk=1)
        close_at = datetime.now()
        auction = Auction(
            title='title',
            current_price=10,
            price_step=1,
            close_at=close_at,
            owner=owner).create()
        self.assertTrue(mock.called)
        auction.current_price = 11
        auction.save()
        self.assertEqual(mock.call_count, 2)
