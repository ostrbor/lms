from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Auction(models.Model):
    title = models.CharField(max_length=200)
    current_price = models.PositiveIntegerField()
    price_step = models.PositiveIntegerField()
    close_at = models.DateTimeField()
    owner = models.ForeignKey(User, related_name='owner')
    winner = models.ForeignKey(
        User, null=True, blank=True, related_name='winner')
    is_opened = models.BooleanField(default=True, db_index=True)


class Bid(models.Model):
    price = models.PositiveIntegerField()
    auction = models.ForeignKey(Auction)
    user = models.ForeignKey(User)
