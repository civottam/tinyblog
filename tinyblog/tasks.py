import smtplib
import datetime
from email.mime.text import MIMEText

from flask_mail import Message

from tinyblog.extensions import flask_celery_helper, mail
from tinyblog.models import Reminder


@flask_celery_helper.task(bind=True, ignore_result=True, default_retry_delay=300, max_retries=5)
def remind(self, primary_key):
    """
    Send a welcome email to user registered just now.
    """
    reminder = Reminder.query.get(primary_key)
    msg = MIMEText(reminder.text)
    msg = Message('Welcome to Tinyblog!', sender="tinyblog@outlook", recipients=[reminder.email])
    msg.body = reminder.text
    mail.send(msg)

def on_reminder_save(mapper, connect, self):
    remind.apply_async(args=(self.id,), eta=self.date)