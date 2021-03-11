from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.tasks.models import Task


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        return context


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        return context


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/profile_confirm_delete.html'

    success_url = '/'


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Account created. Hello {username}. You can no log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request, pk):
    user = User.objects.get(pk=pk)
    if request.user.id != user.id and not request.user.profile.is_user_admin:
        messages.error(
            request, f"Unauthorized, You don't have permissions to do it")
        return redirect('task-list-home')
    else:
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=user)
            p_form = ProfileUpdateForm(
                request.POST, request.FILES, instance=user.profile)

            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Account updated')
                return redirect('profile-user', pk=user.id)
        else:
            u_form = UserUpdateForm(instance=user)
            p_form = ProfileUpdateForm(instance=user.profile)
            if not request.user.profile.is_user_admin:
                del p_form.fields['is_user_admin']
                del p_form.fields['is_task_admin']

        context = {
            'u_form': u_form,
            'p_form': p_form,
        }

        return render(request, 'users/profile_edit.html', context)
