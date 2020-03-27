from dal.test.utils import fixtures
from django.apps import AppConfig
from django.db.models.signals import post_migrate


class ServicesConfig(AppConfig):
    name = 'services'

    def ready(self):
        post_migrate.connect(fixtures, sender=self)
