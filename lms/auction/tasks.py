from django.core.mail import send_mail
from lms.celery import app
from lms.settings import DEFAULT_FROM_EMAIL
import logging

SUBJECT = 'Auction information'

logger = logging.getLogger(__name__)


@app.task
def notify_open_auction(item_description, to_emails: list):
    msg = f'Auction {item_description} is opened.'
    send_mail(SUBJECT, msg, DEFAULT_FROM_EMAIL, to_emails)
    logger.info(f'New auction, sent {len(to_emails)} emails.')


@app.task
def notify_new_bid(item_description, price, to_emails: list):
    msg = f'Auction {item_description} has new price {price}.'
    send_mail(SUBJECT, msg, DEFAULT_FROM_EMAIL, to_emails)
    logger.info(f'New auction bid, sent {len(to_emails)} emails.')


@app.task
def notify_close_auction(item_description, winner, to_emails: list):
    msg = f'Auction {item_description} is closed. Winner is {winner}.'
    send_mail(SUBJECT, msg, DEFAULT_FROM_EMAIL, to_emails)
    logger.info(f'Auction closed, sent {len(to_emails)} emails.')
