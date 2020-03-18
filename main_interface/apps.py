from django.apps import AppConfig
from dal.test.utils import fixtures

from django.db.models.signals import post_migrate


class MainInterfaceConfig(AppConfig):
    name = 'main_interface'

    def ready(self):
        post_migrate.connect(fixtures, sender=self)
