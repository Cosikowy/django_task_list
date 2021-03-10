from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Task(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    worker = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='assigned_tasks')
    status = models.BooleanField(default=False)
    deadline = models.DateTimeField(default=timezone.now)
    file = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk': self.pk})
