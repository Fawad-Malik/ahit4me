import threading
import logging

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


logger = logging.getLogger(__name__)


class EmailThread(threading.Thread):
    def __init__(self, subject, recipient_list, **data):
        self.subject = subject
        self.recipient_list = [recipient_list]
        self.template_name = 'email/template.html'

        self.html_content = render_to_string(self.template_name, data)
        text_content = strip_tags(self.html_content)
        self.text_content = text_content

        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMultiAlternatives(
            self.subject,
            self.text_content,
            'Improve Our World <no-reply@ahit4me.com>',
            self.recipient_list
        )
        msg.attach_alternative(self.html_content, "text/html")
        msg.send()


def send_html_mail(subject, recipient_list, **data):
    EmailThread(subject, recipient_list, **data).start()


def convert_seconds_to_hours(secs):
    if not secs:
        return 0

    hour = secs / 3600

    return float("%.2f" % hour)
