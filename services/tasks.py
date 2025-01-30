import requests
from celery import shared_task

from services.models import Service

BOT_ARTICLE = 'telegram_bot'

class ServiceCommands:
    check_status = 'status'
    restart_service = 'restart'


def try_to_request(tower_command):
    url = f"https://nurbot.kz/tower/{tower_command}"
    headers = {
        'Authorization': 'Token your_secret_token_here',
        'Content-Type': 'application/json',
        'User-Agent': 'insomnia/10.3.0'
    }
    data = {
        "container": "bot_bot-telegram_1"
    }
    response = requests.post(url, headers=headers, json=data)
    return response


@shared_task
def check_status_telegram_bot():
    response = try_to_request(ServiceCommands.check_status)

    if response.status_code == 200:
        response_data = response.json()
        message = response_data.get('message', None)

        if message:
            service = Service.objects.filter(name=BOT_ARTICLE).first()
            service.last_message = message
            service.is_active = True
            service.save()
            return 'Успешно получен ответ'
        return 'Ответ пришел но нет сообщения'
    else:
        try:
            response_data = response.json()
            error = response_data.get('error', None)
        except ValueError:
            error = None

        if error:
            service = Service.objects.filter(name=BOT_ARTICLE).first()
            service.last_message = error
            service.is_active = False
            service.save()
            return "Ответ пришел от Tower но ошибка какая то"

        service = Service.objects.filter(name=BOT_ARTICLE).first()
        resp_data = 'Tower is not available or mistake {}'.format(response.status_code)
        if response.text:
            resp_data += response.text
        service.last_message = resp_data
        service.is_active = False
        service.save()
        return "Ответ не пришел от Tower Tower в опасности"

@shared_task()
def restart_telegram_bot():
    response = try_to_request(ServiceCommands.restart_service)

    if response.status_code == 200:
        response_data = response.json()
        message = response_data.get('message', None)

        if message:
            service = Service.objects.filter(name=BOT_ARTICLE).first()
            service.last_message = message
            service.is_active = True
            service.save()
            return 'Успешно получен ответ'
        return 'Ответ пришел но нет сообщения'
    else:
        try:
            response_data = response.json()
            error = response_data.get('error', None)
        except ValueError:
            error = None

        if error:
            service = Service.objects.filter(name=BOT_ARTICLE).first()
            service.last_message = error
            service.is_active = False
            service.save()
            return "Ответ пришел от Tower но ошибка какая то"

        service = Service.objects.filter(name=BOT_ARTICLE).first()
        resp_data = 'Tower is not available or mistake {}'.format(response.status_code)
        if response.text:
            resp_data += response.text
        service.last_message = resp_data
        service.is_active = False
        service.save()
        return "Ответ не пришел от Tower Tower в опасности"

