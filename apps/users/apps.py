from django.apps import AppConfig
from django.db.models.signals import post_save


class UsersConfig(AppConfig):
    name = 'apps.users'

    def ready(self):
        from apps.users.signals import create_profile, save_profile
        post_save.connect(create_profile, sender=self)
        post_save.connect(save_profile, sender=self)
