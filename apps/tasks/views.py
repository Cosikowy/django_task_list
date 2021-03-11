from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Task
from .forms import TaskForm
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/home.html'
    context_object_name = 'tasks'
    ordering = ['-date_posted']


class TaskdetailView(LoginRequiredMixin, DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    queryset = Task.objects.all()
    form_class = TaskForm
    template_name = 'tasks/task_form.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    permission_required = 'tasks.edit_task'

    def test_func(self):
        return True


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    success_url = '/'

    def test_func(self):
        return True


def about(request):
    return render(request, 'tasks/about.html', {'title': 'About'})
