from django.db import models


class Battery(models.Model):
    serial = models.CharField(max_length=255, verbose_name='Серийный номер', unique=True)

    client = models.ForeignKey('bot.Client', on_delete=models.CASCADE, verbose_name='Клиент')
    seller = models.ForeignKey('bot.Seller', on_delete=models.CASCADE,
                               verbose_name='Продавец', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Зарегистрирован')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')

    latitude = models.FloatField(verbose_name='Широта', null=True, blank=True)
    longitude = models.FloatField(verbose_name='Долгота', null=True, blank=True)

    invoice_telegram_id = models.CharField(max_length=255, verbose_name='Чек', unique=True, null=True,blank=True)
    confirmation_code = models.CharField(max_length=6, verbose_name='Код для продавца',unique=True, null=True, blank=True)
    tech_message = models.TextField(verbose_name='Техническое сообщение', null=True, blank=True)
    def __str__(self):
        return self.serial

class InvoicePhoto(models.Model):
    battery = models.ForeignKey('lottery.Battery', on_delete=models.CASCADE, verbose_name='Аккумулятор')
    photo = models.ImageField(upload_to='invoice_photos/', verbose_name='Фото чека')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.photo


class InvalidTry(models.Model):
    number = models.CharField(max_length=255, verbose_name='Ввод', unique=True)
    telegram_user = models.ForeignKey('bot.UserTelegram', on_delete=models.CASCADE, verbose_name='Телеграм Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"{self.telegram_user.username} - {self.number}"



class TelegramMessage(models.Model):
    telegram = models.ForeignKey('bot.UserTelegram', on_delete=models.CASCADE, verbose_name='Клиент')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.message
