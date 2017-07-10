from django.apps import AppConfig


class APIAppConfig(AppConfig):
    name = 'api'
    label = 'api'
    verbose_name = 'API'

    def ready(self):
        import api.signals


# This is how we register the custom app config with Django.
default_app_config = 'api.APIAppConfig'
