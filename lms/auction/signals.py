from django.db.models.signals import post_save
from django.dispatch import receiver
from auction.models import Auction, User
from auction.tasks import notify_new_bid, notify_open_auction


@receiver(post_save, sender=Auction)
def auction(sender, instance, created, **kwargs):
    emails = User.objects.filter(is_active=True).values_list(
        'email', flat=True)
    # TODO: use delay to use async version of task
    if created:
        notify_open_auction(instance.title, list(emails))
    else:
        notify_new_bid(instance.title, instance.current_price, list(emails))
