from django.contrib import admin
from services.models import Service
from services.tasks import restart_telegram_bot, create_and_send_db_dump


def restart_bot(modeladmin, request, queryset):
    for service in queryset:
        if service.name == 'telegram_bot':
            restart_telegram_bot.delay()
    restart_bot.short_description = 'Перезапустить бота'

def create_dump(modeladmin, request, queryset):

    create_and_send_db_dump.delay()
    create_dump.short_description = 'Сделать Дамп'

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'last_update', 'is_active')
    actions = [restart_bot,create_dump]
