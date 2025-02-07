import time

from celery import shared_task
from bot.bot_core.bot_core import sync_bot
from bot.models import UserTelegram
from lottery.models import MessageTemplate, TelegramMessage


@shared_task
def send_message(telegram_user_id):
    user = UserTelegram.objects.get(telegram_id=telegram_user_id)
    if not user:
        return 'User not found'
    template = MessageTemplate.objects.all().first()
    if not template:
        return 'Template not found'
    result, comment = sync_bot.send_message(user.telegram_id, template.message)
    response = result
    if not result:
        response = comment
    new_message = TelegramMessage.objects.create(telegram=user, message=template.message, response=response)
    new_message.save()
    time.sleep(0.2)
    return f"Message sent: {response} {comment}"