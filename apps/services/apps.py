from django.apps import AppConfig


class ServicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.services'
    verbose_name = 'Service Catalog'

    def ready(self):
        import apps.services.cache  # noqa — register signal handlers
