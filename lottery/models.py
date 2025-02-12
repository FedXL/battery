from django.db import models
class Battery(models.Model):

    serial = models.CharField(max_length=255, verbose_name='Серийный номер', unique=True)
    client = models.ForeignKey('bot.Client', on_delete=models.CASCADE,
                               verbose_name='Клиент',related_name='battery_cli')
    seller = models.ForeignKey('bot.Seller', on_delete=models.CASCADE,
                               verbose_name='Продавец',related_name='battery', null=True, blank=True)
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
    battery = models.ForeignKey(Battery, on_delete=models.CASCADE, verbose_name='Аккумулятор',
                                related_name='invoice_photo')
    photo = models.ImageField(upload_to='invoice_photos/', verbose_name='Фото чека')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return str(self.battery)

class InvalidTry(models.Model):
    number = models.CharField(max_length=255, verbose_name='Ввод', unique=True)
    telegram_user = models.ForeignKey('bot.UserTelegram', on_delete=models.CASCADE, verbose_name='Телеграм Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"{self.telegram_user.username} - {self.number}"

class TelegramMessage(models.Model):
    telegram = models.ForeignKey('bot.UserTelegram', on_delete=models.CASCADE, verbose_name='Клиент')
    message = models.TextField(verbose_name='Сообщение')
    response = models.TextField(verbose_name='Отчет об отправке', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.message

class MessageTemplate(models.Model):
    template_name = models.CharField(max_length=50, verbose_name='Название шаблона', unique=True)
    message = models.TextField(verbose_name='Сообщение')


class LotteryClients(models.Model):
    name = models.CharField(max_length=255, verbose_name='Розыгрыш', unique=True)
    little_prize = models.IntegerField(verbose_name='Количество призов 25000')
    big_prize = models.IntegerField(verbose_name='Количество призов 50000')
    super_prize = models.BooleanField(verbose_name='Розыгрыш 1000000 (если активно разыгрывается среди клиентов '
                                                   'зарегистрировавших хотя бы один аккумулятор',default=False)
    report = models.TextField(verbose_name='Отчет о розыгрыше', null=True, blank=True)



    class Meta:
        verbose_name = 'Розыгрыш среди клиентов'
        verbose_name_plural = 'Розыгрыши среди клиентов'

    def __str__(self):
        return f"{str(self.name)}"


class LotterySellers(models.Model):
    name = models.CharField(max_length=255, verbose_name='Розыгрыш', unique=True)
    little_prize = models.IntegerField(verbose_name='Количество призов 25000')
    report = models.TextField(verbose_name='Отчет о розыгрыше', null=True, blank=True)

    class Meta:
        verbose_name = 'Розыгрыш среди продавцов'
        verbose_name_plural = 'Розыгрыши среди продавцов'

    def __str__(self):
        return str(self.name)




