from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ExportMixin

from bot.resources import BatteryResourses
from lottery.models import (Battery, InvalidTry, TelegramMessage, InvoicePhoto
, MessageTemplate, LotteryClients, LotterySellers)
from lottery.tasks import extract_invoice, clients_lottery_start, sellers_lottery_start


def extract_invoice_check(modeladmin, request, queryset):
    for battery in queryset:
        extract_invoice.delay(battery.id)

def start_client_lottery(modeladmin, request, queryset):
    if queryset.count() > 1:
        return "Выберите только один розыгрыш"
    for lottery in queryset:
        clients_lottery_start.delay(lottery.id)
    start_client_lottery.short_description = "Запуск Розыгрыша для Покупателей"

def start_seller_lottery(modeladmin, request, queryset):
    if queryset.count() > 1:
        return "Выберите только один розыгрыш"
    for lottery in queryset:
        sellers_lottery_start.delay(lottery.id)
    start_seller_lottery.short_description = "Запуск Розыгрыша для Продавцов"



@admin.register(Battery)
class BatteryAdmin(ExportMixin,admin.ModelAdmin):
    list_display = ('serial', 'client', 'seller', 'created_at', 'updated_at')
    readonly_fields = ('confirmation_code', 'tech_message', 'display_invoices')  # Добавляем метод отображения чеков
    search_fields = ('serial', 'client', 'seller')
    actions = [extract_invoice_check]
    def display_invoices(self, obj):
        """Выводит все фото чеков в виде HTML."""
        invoices = InvoicePhoto.objects.filter(battery=obj)
        if not invoices.exists():
            return "Чеков нет"
        images_html = "".join([
            f'<img src="{invoice.photo.url}" width="200" style="margin: 5px; border-radius: 5px;">'
            for invoice in invoices
        ])
        return format_html(images_html)
    display_invoices.short_description = "Фото чеков"
    resource_class = BatteryResourses
@admin.register(InvalidTry)
class InvalidTryAdmin(admin.ModelAdmin):
    list_display = ('number','telegram_user', 'created_at')
    search_fields = ('telegram_user','number')


@admin.register(TelegramMessage)
class TelegramMessageAdmin(admin.ModelAdmin):
    list_display = ('telegram', 'message', 'created_at')
    search_fields = ('telegram_id', 'message')

@admin.register(InvoicePhoto)
class InvoicePhotoAdmin(admin.ModelAdmin):
    list_display = ('battery','created_at')

@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ('template_name', 'message')


@admin.register(LotteryClients)
class LotteryClientsAdmin(admin.ModelAdmin):
    list_display = ('name','little_prize','big_prize')
    actions = [start_client_lottery]

@admin.register(LotterySellers)
class LotterySellersAdmin(admin.ModelAdmin):
    list_display = ('name','little_prize')
    actions = [start_seller_lottery]