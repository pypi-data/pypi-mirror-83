import socket

from flaskel import cap
from flask_mail import Message

from . import celery


@celery.task(bind=True, default_retry_delay=60)
def send_async_email(self, email_data):
    """

    :param self:
    :param email_data:
    """
    try:
        message = Message(
            email_data['subject'],
            sender=cap.config['MAIL_DEFAULT_SENDER'],
            recipients=[
                email_data['to']
            ]
        )
        message.body = email_data['body']
        mail = cap.extensions['mail']

        old_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(60)

        mail.send(message)
        socket.setdefaulttimeout(old_timeout)
    except OSError as exc:
        self.retry(exc=exc)
