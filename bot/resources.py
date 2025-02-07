# resources.py
from import_export import resources
from .models import UserTelegram, Client, ClientProfile, SellerProfile
from import_export import resources, fields

class UserTelegramResource(resources.ModelResource):
    class Meta:
        model = UserTelegram
        fields = ('telegram_id', 'username', 'created_at', 'updated_at')  # Поля, которые экспортируются
        export_order = ('telegram_id', 'username', 'created_at', 'updated_at')  # Порядок полей

class ClientResource(resources.ModelResource):
    class Meta:
        model = Client
        fields = ('user_telegram', 'lottery_winner', 'present_type',)
        export_order = ('user_telegram', 'lottery_winner',)





















class ClientProfileResource(resources.ModelResource):
    # Переопределяем метод для получения telegram_id из связанной модели
    telegram_id = fields.Field(column_name='telegram_id', attribute='client__user_telegram__telegram_id')
    city = fields.Field(column_name='Город', attribute='contact_email')  # Переименование поля


    class Meta:
        model = ClientProfile
        fields = ('telegram_id', 'first_name', 'second_name', 'patronymic', 'contact_phone', 'city', 'language')  # Используем city
        export_order = ('telegram_id', 'first_name', 'second_name', 'patronymic', 'contact_phone', 'city', 'language')  # Указываем порядок


    def dehydrate_telegram_id(self, client_profile):
        return client_profile.client.user_telegram.telegram_id if client_profile.client.user_telegram else None


class SellerProfileResource(resources.ModelResource):
    telegram_id = fields.Field(column_name='telegram_id', attribute='profile__user_telegram__telegram_id')
    city = fields.Field(column_name='Город', attribute='contact_email')

    class Meta:
        model = SellerProfile
        fields = ('telegram_id', 'first_name', 'second_name', 'patronymic', 'contact_phone', 'city', 'language','company_name','company_address')
        export_order = ('telegram_id', 'first_name', 'second_name', 'patronymic', 'contact_phone', 'city', 'language','company_name','company_address')

    def dehydrate_telegram_id(self, seller_profile):
        return seller_profile.seller.user_telegram.telegram_id if seller_profile.seller.user_telegram else None