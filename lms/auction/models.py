from django.db.models.signals import post_save
from django.dispatch import receiver
from auction.tasks import notify_new_bid, notify_open_auction
from rest_framework.authtoken.models import Token
from django.db import models
from django.db.transaction import atomic
from django.contrib.auth import get_user_model

User = get_user_model()


# TODO: replace Int with Decimal
class Auction(models.Model):
    item_description = models.CharField(max_length=200)
    initial_price = models.PositiveIntegerField()
    current_price = models.PositiveIntegerField()
    price_step = models.PositiveIntegerField()
    close_at = models.DateTimeField()
    owner = models.ForeignKey(
        User, related_name='owner', on_delete=models.CASCADE)
    winner = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name='winner',
        on_delete=models.CASCADE)
    is_opened = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return f'{self.item_description}'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.current_price = self.initial_price
        super().save(*args, **kwargs)


# TODO: replace Int with Decimal
class Bid(models.Model):
    price = models.PositiveIntegerField()
    auction = models.ForeignKey(Auction)
    user = models.ForeignKey(User)

    @atomic
    def save(self, *args, **kwargs):
        self.auction.current_price = self.price
        self.auction.save()
        super().save(*args, **kwargs)


def notify_auction_handler(item_description, current_price, emails, created):
    # moved from receiver for testing
    # TODO: use delay to use async version of task
    if created:
        notify_open_auction(item_description, emails)
    else:
        notify_new_bid(item_description, current_price, emails)


@receiver(post_save, sender=Auction)
def notify_post_save_auction(sender, instance, created, **kwargs):
    emails = User.objects.filter(is_active=True).values_list(
        'email', flat=True)
    notify_auction_handler(instance.item_description, instance.current_price,
                           list(emails), created)


def create_token_handler(created, instance):
    # moved from receiver for testing
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_token_post_save_user(sender, instance, created, **kwargs):
    create_token_handler(created, instance)
