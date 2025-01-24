import asyncio
from django.core.management.base import BaseCommand
from bot.management.create_bot import bot
from bot.models import Client
from asgiref.sync import sync_to_async

text = ("Сообщаем, что сегодня, 27 августа 2024 года, в Wildberries были внесены изменения в личный кабинет. "
        "Страницы с коэффициентами приемки подверглись значительным изменениям, что временно сделало наш сервис недоступным. "
        "В настоящее время мы активно работаем над адаптацией системы к новым условиям. "
        "Как только работа будет завершена, мы незамедлительно вас уведомим. Приносим извинения за доставленные неудобства.")



async def alert_to_users():
    clients = await sync_to_async(list)(Client.objects.all())
    for num, client in enumerate(clients, start=1):
        user_id = client.telegram_id
        try:
            message = await bot.send_message(user_id, text)
            print(num, message)
        except Exception as ER:
            print(num, f'error {ER}')


class Command(BaseCommand):
    help = 'Send alert messages to all users'

    def handle(self, *args, **kwargs):
        asyncio.run(alert_to_users())
