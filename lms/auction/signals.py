from django.db.models.signals import post_save
from django.dispatch import receiver
from auction.models import Auction, User
from django.core import mail

import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Auction)
def notify_users(sender, instance, **kwargs):
    emails = User.objects.filter(is_active=True).values_list(
        'email', flat=True)
    results = mail.send_mass_mail(emails)
    logger.debug(results)
