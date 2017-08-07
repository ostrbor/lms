from auction.models import Auction, User
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from auction.tasks import (notify_new_bid, notify_open_auction,
                           notify_close_auction)


def notify_auction_handler(instance, created):
    # moved from receiver for testing
    users = User.objects.filter(is_active=True)
    descr = instance.item_description
    if created:
        auction_owner = instance.owner
        emails = users.exclude(pk=auction_owner.pk).values_list(
            'email', flat=True)
        notify_open_auction.delay(descr, list(emails))
    elif instance.is_opened:
        bid_owner = instance.bids.latest('id').user
        emails = users.exclude(pk=bid_owner.pk).values_list('email', flat=True)
        notify_new_bid.delay(descr, instance.current_price, list(emails))
    elif not instance.is_opened:
        emails = users.values_list('email', flat=True)
        notify_close_auction.delay(descr, instance.winner, list(emails))


@receiver(post_save, sender=Auction)
def notify_post_save_auction(sender, instance, created, **kwargs):
    notify_auction_handler(instance, created)


def create_token_handler(created, instance):
    # moved from receiver for testing
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_token_post_save_user(sender, instance, created, **kwargs):
    create_token_handler(created, instance)
