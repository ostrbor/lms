from django.core.mail import send_mail
from lms.celery import app
from lms.settings import DEFAULT_FROM_EMAIL
import logging

SUBJECT = 'Auction information'

logger = logging.getLogger(__name__)


@app.task
def notify_open_auction(title, to_emails: list):
    msg = f'Auction {title} is opened.'
    send_mail(SUBJECT, msg, DEFAULT_FROM_EMAIL, to_emails)
    logger.info('New auction, sent {len(to_emails)} emails.')


@app.task
def notify_new_bid(title, price, to_emails: list):
    msg = f'Auction {title} has new price {price}.'
    send_mail(SUBJECT, msg, DEFAULT_FROM_EMAIL, to_emails)
    logger.info('New auction bid, sent {len(to_emails)} emails.')


@app.taks
def notify_close_auction(title, winner, to_emails: list):
    msg = f'Auction {title} is closed. Winner is {winner}.'
    send_mail(SUBJECT, msg, DEFAULT_FROM_EMAIL, to_emails)
    logger.info('Auction closed, sent {len(to_emails)} emails.')
