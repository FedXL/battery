from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ExportMixin

from bot.models import UserTelegram, UserWhatsApp, Client, Seller, ClientProfile, SellerProfile
from bot.resources import UserTelegramResource, ClientProfileResource, SellerProfileResource
from bot.tasks import send_message
from lottery.models import Battery


def send_one_message(modeladmin, request, queryset):
    for item in queryset:
        send_message.delay(item.telegram_id)




@admin.register(UserTelegram)
class UserTelegramAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('telegram_id', 'username', 'created_at', 'updated_at')
    search_fields = ('telegram_id', 'username')
    readonly_fields = ('created_at', 'updated_at')
    actions = [send_one_message]  # Ваша пользовательская функция действий
    resource_class = UserTelegramResource


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
    list_display = ('user_telegram', 'lottery_link', 'present_type')
    search_fields = ('user_telegram',)

    def lottery_link(self, obj):
        if obj.lottery_winner:
            url = reverse('admin:lottery_lotteryclients_change', args=[obj.lottery_winner.id])
            return format_html('<a href="{}">{}</a>', url, obj.lottery_winner)
        return '-'

    lottery_link.short_description = 'Lottery Link'
    lottery_link.admin_order_field = 'lottery_winner'


class BatteryInline(admin.TabularInline):
    model = Battery
    fields = ['serial', 'link_to_battery']  # Only show the serial number and a link
    readonly_fields = ['serial', 'link_to_battery']  # Make fields readonly
    extra = 0  # No empty rows for adding new batteries

    def link_to_battery(self, obj):
        # Generate a clickable link to the battery change view
        url = reverse('admin:lottery_battery_change', args=[obj.id])
        return format_html('<a href="{}" target="_blank">{}</a>', url, obj.serial)

    link_to_battery.short_description = 'Battery Link'


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('user_telegram', 'lottery_link', 'present_type', 'rating')
    search_fields = ('user_telegram', 'user_watsapp')
    inlines = [BatteryInline]
    def get_queryset(self, request):
        # Annotate the queryset with the count of related batteries
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(battery_count=Count('battery'))
        return queryset

    def lottery_link(self, obj):
        if obj.lottery_winner:
            url = reverse('admin:lottery_lotterysellers_change', args=[obj.lottery_winner.id])
            return format_html('<a href="{}">{}</a>', url, obj.lottery_winner)
        return '-'

    def rating(self, obj):
        # Return the annotated battery count
        return obj.battery_count

    rating.short_description = 'Рейтинг'
    rating.admin_order_field = 'battery_count'  # Sort by the annotated field
    lottery_link.short_description = 'Lottery Link'
    lottery_link.admin_order_field = 'lottery_winner'

@admin.register(ClientProfile)
class ClientProfileAdmin(ExportMixin,admin.ModelAdmin):
    list_display = ('client', 'first_name', 'second_name', 'patronymic', 'contact_phone', 'contact_email')
    search_fields = ('client__user_telegram__telegram_id',
                     'first_name', 'second_name', 'patronymic', 'contact_phone', 'contact_email')
    resource_class = ClientProfileResource

@admin.register(SellerProfile)
class SellerProfileAdmin(ExportMixin,admin.ModelAdmin):
    list_display = ('seller', 'first_name', 'second_name', 'patronymic', 'contact_phone', 'contact_email')
    search_fields = ('seller__user_telegram__telegram_id',
                     'first_name',
                     'second_name',
                     'patronymic',
                     'contact_phone',
                     'contact_email')

    resource_class = SellerProfileResource