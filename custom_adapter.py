import os
from django.conf import settings
import requests
from allauth.account.adapter import DefaultAccountAdapter
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist
from django.core.mail import EmailMessage, EmailMultiAlternatives
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from allauth.account import app_settings
from ecommerce.env import config
    
    
def send_email(subject, body, recipient):
    msg = MIMEMultipart()
    msg['From'] = config("EMAIL_HOST_USER")
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            context = ssl.create_default_context()
            server.starttls(context=context)
            server.login(
                msg['From'],
                config("EMAIL_HOST_PASSWORD")
            )
            text = msg.as_string()
            
            server.sendmail(
                msg['From'], msg['To'], text)
            print("Email sent successfully")
    except:
        print("Error: unable to send email")



class MyAllauthAdapter(DefaultAccountAdapter):


    def render_mail(self, template_prefix, email, context, headers=None):
        """
        Renders an email to `email`.  `template_prefix` identifies the
        email that is to be sent, e.g. "account/email/email_confirmation"
        """
        to = [email] if isinstance(email, str) else email
        subject = render_to_string("{0}_subject.txt".format(template_prefix), context)
        # remove superfluous line breaks
        subject = " ".join(subject.splitlines()).strip()
        subject = self.format_email_subject(subject)

        from_email = self.get_from_email()

        bodies = {}
        html_ext = app_settings.TEMPLATE_EXTENSION
        for ext in [html_ext, "txt"]:
            try:
                template_name = "{0}_message.{1}".format(template_prefix, ext)
                bodies[ext] = render_to_string(
                    template_name,
                    context,
                ).strip()
            except TemplateDoesNotExist:
                if ext == "txt" and not bodies:
                    # We need at least one body
                    raise
        if "txt" in bodies:
            msg = EmailMultiAlternatives(
                subject, bodies["txt"], from_email, to, headers=headers
            )
            if html_ext in bodies:
                msg.attach_alternative(bodies[html_ext], "text/html")
        else:
            msg = EmailMessage(
                subject, bodies[html_ext], from_email, to, headers=headers
            )
            msg.content_subtype = "html"  # Main content is now text/html
        return msg
    

    def send_mail(self, template_prefix, email, context):
        ctx = {
            "email": email,
        }
        ctx.update(context)
        msg = self.render_mail(template_prefix, email, ctx)
        send_email(msg.subject, msg.body, msg.to[0])