from django.apps import AppConfig


class PhrasesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'phrases'

    class Meta:
        verbose_name = 'Управление контентом'