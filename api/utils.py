from django.core.mail import send_mail
import random
from django.conf import settings

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
#------------------------------------------------------------
def create_random_code(count):
    return random.randint(10**(count-1), 10**count-1)

#------------------------------------------------------------
def send_email(subject, message, to):
    # sender = settings.EMAIL_HOST_USER
    # send_mail(subject, message, sender, to)
    print(100*"#")
    print(subject,message, to )
    print(100*"#")
#------------------------------------------------------------
def send_email_with_html_template(subject, html_message, to, unsubscribe_link):
    email = EmailMessage(subject, strip_tags(html_message), to=to)
    email.attach_alternative(html_message, "text/html")
    email.body = f"{strip_tags(html_message)}\n\nTo unsubscribe, click here: {unsubscribe_link}"
    email.send()