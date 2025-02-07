from django.apps import AppConfig


class LotteryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lottery'

    class Meta:
        verbose_name = 'Лотерея'

    def ready(self):
        import lottery.signals