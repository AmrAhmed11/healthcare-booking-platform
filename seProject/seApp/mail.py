from django.core.mail import EmailMultiAlternatives


# THIS IS AN EXAMPLE FOR SENDING EMAILS

subject = 'Test'
from_email = 'donotreply@seapp.com'
to = 'loay.elshall@icloud.com'
text_content = 'This is a text message.'
html_content = '
This is an HTML message.

'
msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
msg.attach_alternative(html_content, "text/html")
msg.send(fail_silently=False)