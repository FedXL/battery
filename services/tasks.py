import requests
from celery import shared_task
from services.models import Service

import os
import subprocess
from datetime import datetime
from django.conf import settings
from dotenv import load_dotenv
from bot.bot_core.bot_core import sync_bot

load_dotenv()

BOT_ARTICLE = 'telegram_bot'

class ServiceCommands:
    check_status = 'status'
    restart_service = 'restart'


def try_to_request(tower_command):
    url = f"https://nurbot.kz/tower/{tower_command}"
    token = os.getenv('TOWER_TOKEN')
    headers = {
        'Authorization': f'Token {token}',
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

load_dotenv()
CHAT_ID = settings.TELEGRAM_ADMINS
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


@shared_task
def create_and_send_db_dump():
    dump_file_path = f"/tmp/dump_{datetime.now().strftime('%Y%m%d%H%M%S')}.sql"
    try:
        env = os.environ.copy()
        env["PGPASSWORD"] = DB_PASSWORD
        dump_command = [
            "pg_dump",
            "-h", DB_HOST,
            "-p", str(DB_PORT),
            "-U", DB_USER,
            "-F", "c",
            "-b",
            "-v",
            "-f", dump_file_path,
            DB_NAME]
        subprocess.run(dump_command, check=True, env=env)

        with open(dump_file_path, "rb") as dump_file:
            for chat in CHAT_ID:
                sync_bot.send_document(chat_id=chat, document=dump_file)
            print(f"Database dump sent to Telegram chat {CHAT_ID}")

    except subprocess.CalledProcessError as e:
        print(f"Error creating database dump: {e}")
    except Exception as e:
        print(f"Error sending dump file via Telegram: {e}")
    finally:
        if os.path.exists(dump_file_path):
            os.remove(dump_file_path)
            print(f"Deleted dump file: {dump_file_path}")


