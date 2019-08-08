from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

from django.conf import settings
def send_verification_email(email,link):

    subject, from_email, to = 'Verificate Email', settings.EMAIL_HOST_USER, email
    text_content = 'Verificate Email.'
    html_content = f'<p>Please verify this link <a href="{link}">Link</a></p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    pass