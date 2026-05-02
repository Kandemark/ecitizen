from django.apps import AppConfig


class CivilRegistryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.civil_registry'
    verbose_name = 'Civil Registry (Births, Deaths, Marriages)'
