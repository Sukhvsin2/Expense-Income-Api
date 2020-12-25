from django.core.mail import EmailMessage, send_mail
import smtplib
import os

class Util:
    @staticmethod
    def send_email(data):
        # email = EmailMessage(subject=data['email_subject'], body=data['email_body'], to=[data['email_to']])
        # email.send()
        # send_mail(
        #     data['email_subject'],
        #     data['email_body'],
        #     str(os.getenv('EMAIL_HOST_USER')),
        #     [data['email_to']],
        # )
        server = smtplib.SMTP('smtp.gmail.com', 25)
        server.connect("smtp.gmail.com", 587)
        server.ehlo()
        server.login(os.getenv('EMAIL_HOST_USER'), os.getenv('EMAIL_HOST_PASSWORD'))
        text = data['email_body']
        server.sendmail(os.getenv('EMAIL_HOST_USER'), data['email_to'], text)
        server.quit()