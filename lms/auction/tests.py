from django.test import TestCase
from unittest.mock import patch, MagicMock
from auction.models import Auction, User, Bid
import datetime
from auction.serializers import BidCreateSerializer
from rest_framework.serializers import ValidationError
from auction.tasks import close_auctions


class GeneralTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.email_patch = patch('auction.signals.notify_auction_handler')
        cls.email = cls.email_patch.start()

    @classmethod
    def tearDownClass(cls):
        cls.email_patch.stop()

    def setUp(self):
        self.auction_owner = User.objects.create_user(
            username='User', password='123', email='user@gmail.com')
        close_at = datetime.datetime.now()
        self.auction = Auction(
            item_description='item_description',
            initial_price=10,
            price_step=1,
            close_at=close_at,
            owner=self.auction_owner)
        self.bid_user = User.objects.create_user(
            username='Bid User', password='123', email='biduser@gmail.com')


class SignalsTestCase(GeneralTestCase):
    @patch('django.db.models.signals.post_save.send')
    def test_post_save_signal_triggered(self, mock):
        # NOTE: redundant test
        self.auction.save()
        self.assertTrue(mock.called)

    def test_signal_handler_notify_auction_triggered(self):
        self.auction.save()
        self.assertTrue(self.email.called)

    def test_bid_save_updates_auction_price(self):
        self.auction.save()
        bid = Bid(price=11, auction=self.auction, user=self.auction_owner)
        bid.save()
        self.auction.refresh_from_db()
        self.assertEqual(self.auction.current_price, bid.price)


class BidCreateSerializerTestCase(GeneralTestCase):
    def test_validate_raises_auction_closed(self):
        self.auction.is_opened = False
        self.auction.save()
        data = {'id': 1, 'price': 11, 'auction': 1}
        ser = BidCreateSerializer(data=data)
        with self.assertRaises(ValidationError):
            ser.is_valid(raise_exception=True)

    def test_validate_raises_same_auction_bid_user(self):
        data = {'id': 1, 'price': 11, 'auction': 1}
        request_mock = MagicMock(user=self.auction_owner)
        ser = BidCreateSerializer(data=data, context={'request': request_mock})
        with self.assertRaises(ValidationError):
            ser.is_valid(raise_exception=True)

    def test_validate_raises_bid_price_lower_auction_price(self):
        data = {'id': 1, 'price': 9, 'auction': 1}
        request_mock = MagicMock(user=self.bid_user)
        ser = BidCreateSerializer(data=data, context={'request': request_mock})
        with self.assertRaises(ValidationError):
            ser.is_valid(raise_exception=True)

    def test_validate_raises_not_used_price_step(self):
        data = {'id': 1, 'price': 11.5, 'auction': 1}
        request_mock = MagicMock(user=self.bid_user)
        ser = BidCreateSerializer(data=data, context={'request': request_mock})
        with self.assertRaises(ValidationError):
            ser.is_valid(raise_exception=True)


class CloseAuctionTaskTestCase(GeneralTestCase):
    def setUp(self):
        super().setUp()
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        self.auction.close_at = yesterday
        self.auction.save()

    def test_task_set_is_opened_to_false(self):
        self.assertTrue(self.auction.is_opened)
        close_auctions()
        self.auction.refresh_from_db()
        self.assertFalse(self.auction.is_opened)

    def test_task_set_winner(self):
        Bid(user=self.bid_user, price=12, auction=self.auction).save()
        close_auctions()
        self.auction.refresh_from_db()
        self.assertEqual(self.auction.winner, self.bid_user)
