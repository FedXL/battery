from django.contrib import admin

from lottery.models import Battery, InvalidTry,TelegramMessage


# Register your models here.
@admin.register(Battery)
class BatteryAdmin(admin.ModelAdmin):
    list_display = ('serial', 'client', 'seller', 'created_at', 'updated_at')
    readonly_fields = ('confirmation_code','tech_message')
    search_fields = ('serial', 'client', 'seller')


@admin.register(InvalidTry)
class InvalidTryAdmin(admin.ModelAdmin):
    list_display = ('number','telegram_user', 'created_at')
    search_fields = ('telegram_user','number')


@admin.register(TelegramMessage)
class TelegramMessageAdmin(admin.ModelAdmin):
    list_display = ('telegram', 'message', 'created_at')
    search_fields = ('telegram_id', 'message')