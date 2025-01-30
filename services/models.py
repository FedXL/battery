from django.db import models

# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name='Артикул',unique=True)
    description = models.TextField(verbose_name='Описание')
    last_update = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    last_message = models.TextField(null=True, blank=True, verbose_name='Последнее сообщение')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'
