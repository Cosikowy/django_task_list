from django import forms
from django.utils import timezone
from .models import Task


class TaskForm(forms.ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = Task
        fields = ['title', 'content', 'worker', 'deadline']
