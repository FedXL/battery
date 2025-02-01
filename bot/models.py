from django.core.exceptions import ValidationError
from django.db import models

class UserTelegram(models.Model):
    telegram_id = models.BigIntegerField(primary_key=True, unique=True, verbose_name='ID телеграмма')
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name='Имя пользователя')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата Последнего посещения')

    def __str__(self):
        return str(self.telegram_id)

    class Meta:
        verbose_name = 'telegram user'
        verbose_name_plural = 'telegram users'

class UserWhatsApp(models.Model):
    phone_watsapp = models.BigIntegerField(primary_key=True, unique=True, verbose_name='ID WhatsApp')
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name='Имя пользователя')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата Последнего посещения')

    class Meta:
        verbose_name = 'WhatsApp user'
        verbose_name_plural = 'WhatsApp users'

class ClientBase(models.Model):
    user_telegram = models.OneToOneField(UserTelegram, on_delete=models.CASCADE,
                                         verbose_name='Телеграм Пользователь',null=True, blank=True)
    user_watsapp = models.OneToOneField(UserWhatsApp, on_delete=models.CASCADE,verbose_name='Вотсапп Пользователь',
                                        null=True, blank=True)
    class Meta:
        abstract = True

    def clean(self):
        if not self.user_telegram and not self.user_watsapp:
            raise ValidationError('Укажите хотя бы одного пользователя')

    def __str__(self):
        return f"{self.user_telegram}"

class Client(ClientBase):
    verbose_name = 'клиент связь с ботом'
    verbose_name_plural = 'клиенты связи с ботом'



class Seller(ClientBase):
    verbose_name = 'продавец связь с ботом'
    verbose_name_plural = 'продавцы связи с ботом'


class Message(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')


class ProfileBase(models.Model):
    phone_from_telegram = models.CharField(max_length=255, null=True, blank=True, verbose_name='Телефон привязанный к телеграм аккаунту')
    first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Имя')
    second_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=255, null=True, blank=True, verbose_name='Отчество')
    contact_phone = models.CharField(max_length=255, null=True, blank=True, verbose_name='Контактный телефон')
    contact_email = models.EmailField(null=True, blank=True, verbose_name='Город')

    language = models.CharField(max_length=255, null=True, blank=True, verbose_name='Язык')

    class Meta:
        abstract = True



class ClientProfile(ProfileBase):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    class Meta:
        verbose_name = 'Профиль клиента'
        verbose_name_plural = 'Профили клиентов'

    def __str__(self):
        return f"{self.client} | {self.first_name} {self.second_name}"
class SellerProfile(ProfileBase):
    seller = models.OneToOneField(Seller, on_delete=models.CASCADE, verbose_name='Продавец')

    company_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='Адрес компании')
    company_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Название компании')


    class Meta:
        verbose_name = 'Профиль продавца'
        verbose_name_plural = 'Профили продавцов'

    def __str__(self):
        return f"{self.seller} | {self.first_name} {self.second_name}"