from django.db import models
from django.db.transaction import atomic
from django.contrib.auth import get_user_model

User = get_user_model()


class Auction(models.Model):
    item_description = models.CharField(max_length=200)
    initial_price = models.DecimalField(max_digits=11, decimal_places=2)
    current_price = models.DecimalField(max_digits=11, decimal_places=2)
    price_step = models.DecimalField(max_digits=11, decimal_places=2)
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


class Bid(models.Model):
    price = models.DecimalField(max_digits=11, decimal_places=2)
    auction = models.ForeignKey(Auction, related_name='bids')
    user = models.ForeignKey(User)

    @atomic
    def save(self, *args, **kwargs):
        self.auction.current_price = self.price
        self.auction.save()
        super().save(*args, **kwargs)
