

from django.core.mail import send_mail 
from django.conf import settings
from django.template.loader import render_to_string
from smtplib import SMTPException

from rest_framework import serializers



def user_create_mail(email, activation_code):
        email_subject = "Account Creation Successful"
        email_from = settings.EMAIL_HOST_USER

        context = ({'name': 'Ekene', 'activation_code': activation_code})

        text_content = render_to_string('create_email.txt', context)

        try:
                send_mail(email_subject, text_content, email_from, [email])

        except SMTPException as e:
                print( 'There was an error sending this email', e)
                error = {'message': ",".join(e.args) if len(e.args) < 0 else "Unknown Error"}
                raise serializers.ValidationError(error)



def reset_password_mail(email, reset_code):
        email_subject = "Reset Password"
        email_from = settings.EMAIL_HOST_USER

        context = ({'reset_code': reset_code})

        text_content = render_to_string('reset_password.txt', context)

        try:
                send_mail(email_subject, text_content, email_from, email)

        except SMTPException as e:
                print( 'There was an error sending this email', e)
                error = {'message': ",".join(e.args) if len(e.args) > 0 else "Unknown Error"}
                raise serializers.ValidationError(error)
        

