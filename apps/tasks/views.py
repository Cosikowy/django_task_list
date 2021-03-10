from django.shortcuts import render
from .models import Task
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/home.html'
    context_object_name = 'tasks'
    ordering = ['-date_posted']


class TaskdetailView(LoginRequiredMixin, DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.author:
            return True
        return False


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    success_url = '/'

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.author:
            return True
        return False


def about(request):
    return render(request, 'tasks/about.html', {'title': 'About'})
