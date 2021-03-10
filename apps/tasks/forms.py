from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = Task
        fields = ['title', 'content', 'worker', 'deadline', 'status']
