from celery import shared_task
from django.core.mail import send_mass_mail
from .models import Task
from django.template.loader import render_to_string


@shared_task
def send_emails(*args, **kwargs):
    send_mass_mail(*args, **kwargs)


def check_tasks_daily():
    tasks = Task.objects.all()
    emails_to_send = []

    for task in tasks:
        if not task.status:
            email_context = {'task': task}
            email_template = render_to_string(
                'tasks/email.html', context=email_context)
            emails_to_send.append(
                (
                    task.title,
                    email_template,
                    None,
                    [task.worker.email]
                )
            )
    send_emails(tuple(emails_to_send), fail_silently=False)
