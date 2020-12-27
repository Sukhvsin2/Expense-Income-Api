from django.core.mail import EmailMessage, send_mail
import smtplib, ssl
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

        try:
            port = 587  # For starttls
            smtp_server = "smtp.gmail.com"
            sender_email = "djangotestingemail07@gmail.com"
            receiver_email = data['email_to']
            password = '9582844619'
            message = "Subject: Hi there\n" + data['email_body']

            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, port) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)
        except: 
            print('failed')