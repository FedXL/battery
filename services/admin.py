from django.contrib import admin
from services.models import Service
from services.tasks import restart_telegram_bot

def restart_bot(modeladmin, request, queryset):
    for service in queryset:
        if service.name == 'telegram_bot':
            restart_telegram_bot.delay()
    restart_bot.short_description = 'Перезапустить бота'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'last_update', 'is_active')
    actions = [restart_bot]
