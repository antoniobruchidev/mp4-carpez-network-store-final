import os
from django.conf import settings
import requests
from allauth.account.adapter import DefaultAccountAdapter
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist
from django.core.mail import EmailMessage, EmailMultiAlternatives
from allauth.account import app_settings
from django.contrib.sites.shortcuts import get_current_site
from ecommerce.env import config



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
        url = config('EMAIL_RELAY_URL')
        post_data = [
            ('subject', msg.subject),
            ('recipient', msg.to[0]),
            ('body', msg.body),
            ('sender', msg.from_email),
            ('secret', config("FLASK_RELAY_SECRET"))]
            
        result = requests.post(url, data=post_data)