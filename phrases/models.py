from django.db import models


class OnlyReplies(models.Model):
    name = models.CharField(max_length=255, verbose_name='Переменная', unique=True)
    description = models.CharField(verbose_name='Описание', null=True, blank=True)

    kaz = models.TextField(verbose_name='текст на Казахском')
    rus = models.TextField(verbose_name='текст на Русском')

    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата Последнего посещения')
    is_checked = models.BooleanField(default=False, verbose_name='Проверено')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Реплика'
        verbose_name_plural = 'Реплики'