from django.apps import AppConfig


class HouseMlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'HOUSE_ML'



class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'HOUSE_ML'

    # add this
    def ready(self):
        import signals  # noqa