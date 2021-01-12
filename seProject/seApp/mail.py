# from django.core.mail import EmailMultiAlternatives
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags



# THIS IS AN EXAMPLE FOR SENDING EMAILS
def sendEmail(subject,to,mail_template):
    from_email = 'seApp <1701043@eng.asu.edu.eg>'
    paragraph = "test"
    html_message = render_to_string('seApp/mail_temps/' + mail_template + '.html', {'context': paragraph})
    plain_message = strip_tags(html_message)
    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)