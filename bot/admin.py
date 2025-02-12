from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from import_export.admin import ExportMixin
from bot.bot_core.collections.variables import Templates
from bot.models import UserTelegram, UserWhatsApp, Client, Seller, ClientProfile, SellerProfile
from bot.resources import UserTelegramResource, ClientResource, \
    SellerResource
from bot.tasks import send_message
from lottery.models import Battery


def send_one_message(modeladmin, request, queryset):
    for item in queryset:
        send_message.delay(item.telegram_id, Templates.random_message)
send_one_message.short_description = "Отправить сообщение"

def send_one_message_for_client_or_seller(modeladmin, request, queryset):
    for item in queryset:
        send_message.delay(item.user_telegram.telegram_id, Templates.random_message)
send_one_message_for_client_or_seller.short_description = 'Отправить сообщение'


def send_one_message_for_clientprofile(modeladmin, request, queryset):
    for item in queryset:
        send_message.delay(item.client.user_telegram.telegram_id, Templates.random_message)
send_one_message_for_clientprofile.short_description = "Отправить сообщение"

def send_one_message_for_sellerprofile(modeladmin, request, queryset):
    for item in queryset:
        send_message.delay(item.seller.user_telegram.telegram_id, Templates.random_message)
send_one_message_for_sellerprofile.short_description = "Отправить сообщение"

@admin.register(UserTelegram)
class UserTelegramAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('telegram_id', 'username', 'created_at', 'updated_at')
    search_fields = ('telegram_id', 'username')
    readonly_fields = ('created_at', 'updated_at')
    actions = [send_one_message]
    resource_class = UserTelegramResource


@admin.register(UserWhatsApp)
class UserWhatsAppAdmin(admin.ModelAdmin):
    list_display = ('phone_watsapp', 'username', 'created_at', 'updated_at')
    search_fields = ('phone_watsapp', 'username')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


class ClientProfileInline(admin.StackedInline):
    model = ClientProfile
    extra = 0


class SellerProfileInline(admin.StackedInline):
    model = SellerProfile
    extra = 0

class BatteryInline(admin.TabularInline):
    model = Battery
    fields = ['serial', 'link_to_battery']
    readonly_fields = ['serial', 'link_to_battery']
    extra = 0

    def link_to_battery(self, obj):

        url = reverse('admin:lottery_battery_change', args=[obj.id])
        return format_html('<a href="{}" target="_blank">{}</a>', url, obj.serial)

    link_to_battery.short_description = 'Battery Link'


@admin.register(Client)
class ClientAdmin(ExportMixin,admin.ModelAdmin):
    list_display = ('user_telegram', 'lottery_link', 'present_type')
    search_fields = ('user_telegram__telegram_id',)
    actions = [send_one_message_for_client_or_seller]
    def lottery_link(self, obj):
        if obj.lottery_winner:
            url = reverse('admin:lottery_lotteryclients_change', args=[obj.lottery_winner.id])
            return format_html('<a href="{}">{}</a>', url, obj.lottery_winner)
        return '-'

    inlines = [BatteryInline, ClientProfileInline]
    lottery_link.short_description = 'Lottery Link'
    lottery_link.admin_order_field = 'lottery_winner'
    resource_class = ClientResource


@admin.register(Seller)
class SellerAdmin(ExportMixin,admin.ModelAdmin):
    list_display = ('user_telegram', 'lottery_link', 'present_type', 'rating')
    search_fields = ('user_telegram__telegram_id',)
    inlines = [BatteryInline, SellerProfileInline]
    actions = [send_one_message_for_client_or_seller]
    resource_class = SellerResource
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(battery_count=Count('battery'))
        return queryset


    def lottery_link(self, obj):
        if obj.lottery_winner:
            url = reverse('admin:lottery_lotterysellers_change', args=[obj.lottery_winner.id])
            return format_html('<a href="{}">{}</a>', url, obj.lottery_winner)
        return '-'

    def rating(self, obj):
        return obj.battery_count

    rating.short_description = 'Рейтинг'
    rating.admin_order_field = 'battery_count'
    lottery_link.short_description = 'Lottery Link'
    lottery_link.admin_order_field = 'lottery_winner'



@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('client', 'first_name', 'second_name', 'patronymic',
                    'contact_phone', 'contact_email')
    search_fields = ('client__user_telegram__telegram_id',
                     'first_name', 'second_name', 'patronymic', 'contact_phone', 'contact_email')

    actions = [send_one_message_for_clientprofile]


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):

    list_display = ('seller', 'first_name', 'second_name', 'patronymic', 'contact_phone', 'contact_email')
    search_fields = ('seller__user_telegram__telegram_id',
                     'first_name',
                     'second_name',
                     'patronymic',
                     'contact_phone',
                     'contact_email')

    actions = [send_one_message_for_sellerprofile]