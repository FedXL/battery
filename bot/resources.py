# resources.py
from lottery.models import Battery
from .models import UserTelegram, Client, ClientProfile, SellerProfile, Seller
from import_export import resources, fields

class UserTelegramResource(resources.ModelResource):
    class Meta:
        model = UserTelegram
        fields = ('telegram_id', 'username', 'created_at', 'updated_at')  # Поля, которые экспортируются
        export_order = ('telegram_id', 'username', 'created_at', 'updated_at')  # Порядок полей




class ClientResource(resources.ModelResource):


    lottery_winner = fields.Field(
        column_name='Победитель',
        attribute='lottery_winner')
    present_type = fields.Field(
        column_name='Тип приза',
        attribute='present_type')


    profile_first_name = fields.Field(
        column_name='Имя',
        attribute='clientprofile__first_name'
    )
    profile_second_name = fields.Field(
        column_name='Фамилия',
        attribute='clientprofile__second_name'
    )
    profile_patronymic = fields.Field(
        column_name='Отчество',
        attribute='clientprofile__patronymic'
    )
    profile_contact_phone = fields.Field(
        column_name='Контактный телефон',
        attribute='clientprofile__contact_phone'
    )
    profile_contact_email = fields.Field(
        column_name='Город',
        attribute='clientprofile__contact_email'
    )
    profile_language = fields.Field(
        column_name='Язык',
        attribute='clientprofile__language'
    )
    telegram_id = fields.Field(
        column_name='Telegram ID',
        attribute='user_telegram__telegram_id'
    )

    rating = fields.Field(
        column_name='Количество батарей')


    class Meta:
        model = Client
        fields = (
            'telegram_id',
            'lottery_winner',
            'present_type',
            'profile_first_name',
            'profile_second_name',
            'profile_patronymic',
            'profile_contact_phone',
            'profile_contact_email',
            'profile_language',
            'rating',
        )
        export_order = (
            'telegram_id',
            'lottery_winner',
            'present_type',
            'profile_first_name',
            'profile_second_name',
            'profile_patronymic',
            'profile_contact_phone',
            'profile_contact_email',
            'profile_language',
            'rating',
        )

    def get_queryset(self):
        return (
            Client.objects.select_related('clientprofile', 'user_telegram')# Подсчет батарей
        )

    def dehydrate_rating(self, client):
        total_batteries = client.battery_cli.count()


        return total_batteries


class SellerResource(resources.ModelResource):
    lottery_winner = fields.Field(
        column_name='Победитель',
        attribute='lottery_winner')

    present_type = fields.Field(
        column_name='Тип приза',
        attribute='present_type')

    profile_first_name = fields.Field(
        column_name='Имя',
        attribute='sellerprofile__first_name'
    )
    profile_second_name = fields.Field(
        column_name='Фамилия',
        attribute='sellerprofile__second_name'
    )
    profile_patronymic = fields.Field(
        column_name='Отчество',
        attribute='sellerprofile__patronymic'
    )
    profile_contact_phone = fields.Field(
        column_name='Контактный телефон',
        attribute='sellerprofile__contact_phone'
    )
    profile_contact_email = fields.Field(
        column_name='Город',
        attribute='sellerprofile__contact_email'
    )
    profile_language = fields.Field(
        column_name='Язык',
        attribute='sellerprofile__language'
    )
    telegram_id = fields.Field(
        column_name='Telegram ID',
        attribute='user_telegram__telegram_id'
    )
    rating = fields.Field(
        column_name='Количество батарей'
    )

    class Meta:
        model = Seller
        fields = (
            'telegram_id',
            'lottery_winner',
            'present_type',
            'company_address',
            'company_name',
            'profile_first_name',
            'profile_second_name',
            'profile_patronymic',
            'profile_contact_phone',
            'profile_contact_email',
            'profile_language',
            'rating'
        )
        export_order = (
            'telegram_id',
            'lottery_winner',
            'present_type',
            'company_address',
            'company_name',
            'profile_first_name',
            'profile_second_name',
            'profile_patronymic',
            'profile_contact_phone',
            'profile_contact_email',
            'profile_language',
            'rating'
        )

    def get_queryset(self):
        return (
            Seller.objects.select_related('sellerprofile', 'user_telegram')
        )

    def dehydrate_rating(self, seller):
        total_batteries = seller.battery_set.count()
        return total_batteries



class BatteryResourses(resources.ModelResource):

    client = fields.Field(
        column_name='Client',
        attribute='client__user_telegram__telegram_id'
    )
    seller = fields.Field(
        column_name='Seller',
        attribute='seller__user_telegram__telegram_id'
    )

    class Meta:
        model = Battery
        fields = ('serial','client', 'seller', 'created_at', 'updated_at')
        export_order = ('serial', 'client', 'seller', 'created_at', 'updated_at')  # Порядок полей