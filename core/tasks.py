from celery import shared_task
from django.core.mail import send_mail
from FreJunTeamTaskDjango.settings import EMAIL_HOST_USER


@shared_task(name="sum_two_numbers")
def add(x, y):
    return x + y


@shared_task(name="send_mail")
def send_mail_to(subject, msg, recievers):

    send_mail(
        subject,
        msg,
        EMAIL_HOST_USER,
        recievers,
        fail_silently=False,
    )