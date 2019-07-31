from django.core.mail import send_mail
import logging

def sendmail(recipient_list, subject=None, message=None,
             from_email=None,fail_silently=False, html_message=None):
    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently, html_message)
        return True
    except Exception as e:
        logging.error(e)
        return False