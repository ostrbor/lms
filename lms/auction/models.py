from django.db.models.signals import post_save
from django.dispatch import receiver
from auction.tasks import notify_new_bid, notify_open_auction
from rest_framework.authtoken.models import Token
from django.db import models
from django.db.transaction import atomic
from django.contrib.auth import get_user_model

User = get_user_model()


# TODO: replace title with description
# TODO: add base_price
# TODO: replace Int with Decimal
class Auction(models.Model):
    title = models.CharField(max_length=200)
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
        return f'{self.title}'


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


# TODO: rename to 'notify_auction'
@receiver(post_save, sender=Auction)
def auction(sender, instance, created, **kwargs):
    emails = User.objects.filter(is_active=True).values_list(
        'email', flat=True)
    # TODO: use delay to use async version of task
    if created:
        notify_open_auction(instance.title, list(emails))
    else:
        notify_new_bid(instance.title, instance.current_price, list(emails))


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
