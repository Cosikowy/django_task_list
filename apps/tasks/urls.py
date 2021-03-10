from django.urls import path
from . import views
from .views import (TaskListView,
                    TaskdetailView,
                    TaskCreateView,
                    TaskUpdateView,
                    TaskDeleteView
                    )


urlpatterns = [
    path('', TaskListView.as_view(), name='task-list-home'),
    path('about/', views.about, name='task-list-about'),
    path('task/<int:pk>/', TaskdetailView.as_view(), name='task-detail'),
    path('task/new/', TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/update', TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/delete', TaskDeleteView.as_view(), name='task-delete'),


]
