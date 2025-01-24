from django.contrib import admin
from bot.models import UserTelegram, UserWhatsApp, Client, Seller, ClientProfile, SellerProfile

@admin.register(UserTelegram)
class UserTelegramAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'username', 'created_at', 'updated_at')
    search_fields = ('telegram_id', 'username')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(UserWhatsApp)
class UserWhatsAppAdmin(admin.ModelAdmin):
    list_display = ('phone_watsapp', 'username', 'created_at', 'updated_at')
    search_fields = ('phone_watsapp', 'username')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

class ClientProfileInline(admin.TabularInline):
    model = ClientProfile
    extra = 0

class SellerProfileInline(admin.TabularInline):
    model = SellerProfile
    extra = 0

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user_telegram', 'user_watsapp')
    search_fields = ('user_telegram', 'user_watsapp')

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('user_telegram', 'user_watsapp')
    search_fields = ('user_telegram', 'user_watsapp')

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('client', 'first_name', 'second_name', 'patronymic', 'contact_phone', 'contact_email')
    search_fields = ('client', 'first_name', 'second_name', 'patronymic', 'contact_phone', 'contact_email')

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('seller', 'first_name', 'second_name', 'patronymic', 'contact_phone', 'contact_email')
    search_fields = ('seller', 'first_name', 'second_name', 'patronymic', 'contact_phone', 'contact_email')