from auction.models import Auction, User
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from auction.tasks import notify_new_bid, notify_open_auction, notify_close_auction


def notify_auction_handler(instance, emails, created):
    # moved from receiver for testing
    # TODO: use delay to use async version of task
    descr = instance.item_description
    if created:
        notify_open_auction(descr, emails)
    elif instance.is_opened:
        notify_new_bid(descr, instance.current_price, emails)
    elif not instance.is_opened:
        notify_close_auction(descr, instance.winner, emails)


@receiver(post_save, sender=Auction)
def notify_post_save_auction(sender, instance, created, **kwargs):
    emails = User.objects.filter(is_active=True).values_list(
        'email', flat=True)
    notify_auction_handler(instance, list(emails), created)


def create_token_handler(created, instance):
    # moved from receiver for testing
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_token_post_save_user(sender, instance, created, **kwargs):
    create_token_handler(created, instance)
