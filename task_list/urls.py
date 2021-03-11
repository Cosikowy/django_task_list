"""snippets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from apps.users import views as user_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('', include('apps.tasks.urls')),
    path('profile/<int:pk>/edit', user_views.profile, name='profile-edit'),
    path('profile/<int:pk>/', user_views.UserProfileView.as_view(),
         name='profile-user'),
    path('profile/<int:pk>/delete',
         user_views.ProfileDeleteView.as_view(), name='profile-delete'),

    path('users/', include('apps.users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
