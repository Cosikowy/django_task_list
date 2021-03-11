import os
from datetime.datetime import date
from django.template.loader import render_to_string
from django.core.mail import send_mass_mail
from celery import shared_task

from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_list.settings')

# set the default Django settings module for the 'celery' program.

app = Celery('tasks_list')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(
        crontab(hour=0, minute=0),
        check_tasks_daily.s(),
    )

    sender.add_periodic_task(
        crontab(hour=0, minute=0),
        check_deadlines.s(),
    )


@app.task
def test(arg):
    print(arg)


@shared_task
def check_tasks_daily():
    from apps.tasks.models import Task
    tasks = Task.objects.all()
    emails_to_send = []
    unfinished = []
    for task in tasks:
        if not task.status:
            unfinished.append(task)

    email_context = {'tasks': unfinished, 'title': 'Daily task info!'}
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
    send_mass_mail(tuple(emails_to_send), fail_silently=False)


@shared_task
def check_deadlines():
    from apps.tasks.models import Task
    tasks = Task.objects.all()
    emails_to_send = []
    for task in tasks:
        if task.deadline > date.today():
            email_context = {'tasks': task, 'title': 'You missed the deadline'}
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
    send_mass_mail(tuple(emails_to_send), fail_silently=False)
