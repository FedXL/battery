import requests
from bot.management.bot_core.handlers.bot_utils import bot_urls as U
from fusion_core.settings import BOT_TOKEN, fedor_id


def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "MarkdownV2"}
    response=requests.post(url, data=data)
    print(response.status_code)
    print(response.json())

def error_warning_handler(text):
    print('start parser')
    send_message(fedor_id, text)

def execute_task_handler(data: dict):
    print('START EXECUTE TASK HANDLER')
    TOKEN = BOT_TOKEN
    for key, value in data.items():
        text = (
            f"🔔🔔🔔 <b>День найден! №{key}</b> 🔔🔔🔔\n\n"
            f"🔸Дата: <b>{value['find_day']}</b>.\n"
            f"🔸Найденный коэффициент: <b>{value['parser_coefficient']}</b>.\n\n"
            f"Детали задания:\n"
            f"  🔹Склад: {value['warehouse_name']}.\n"
            f"  🔹Тип поставки: {value['delivery_type']}.\n"
            f"  🔹Поиск был осуществлен по коэффициенту: {value['task_coefficient']} и менее.\n"
            f"  🔹Поиск был осуществлен в течение следующих дней: {value['task_days']}.\n"
        )
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {
            "chat_id": value['telegram_id'],
            "text": text,
            "parse_mode": "HTML",
            "reply_markup": {
                "inline_keyboard": [[
                    {
                        "text": "Убрать☠️",  # Текст вашей кнопки
                        "callback_data": "kill_myself"  # Данные для колбека
                    },
                    {
                        "text": "Go to Wildberries",
                        "url": "https://seller.wildberries.ru/supplies-management/all-supplies"
                    }
                ]]
            }
        }
        response_telegram = requests.post(url, json=data)
        if response_telegram.status_code == 200:
            print(f"Message sent to {value['telegram_id']}")
        else:
            print(f"Error sending message to {value['telegram_id']}")
        kill_day_or_task_success_handler(value=value)
    return None


def kill_day_or_task_success_handler(value):
    """1. Удалить день из таски. При этом если дней не осталось удалить таску."""
    print('[SUCCESS KILLER] starting way')
    day_id = value['day_id']
    day = value['find_day']
    days: list = value['task_days']
    if day in days:
        days.remove(day)
    print(days,len(days))
    if len(days) == 0:
        print("[SUCCESS KILLER] we need to kill task")
        response_django = requests.delete(U.URL_TASK + f"{value['task_id']}/?client={value['telegram_id']}")
        print('RESPONSE', response_django.status_code)
        if response_django.status_code == 204:
            print('ok success message ')
            kill_task_send_message_positive(value)
        else:
            print(f"Error deleting task {value['task_id']}")
    else:
        print('Осталось дней', len(days), days)
        print(len(days), days)
        url = U.URL_TASK_DATES + f"{day_id}/"
        print(url)
        response_django = requests.delete(url=url)
        if response_django.status_code == 204:
            print(f"Day was deleted")
        else:
            print(response_django.status_code)
            print(f"Error deleting day")


def kill_task_send_message_positive(value):
    """После удаления таски отправить сообщение о том что таска полностью отработала"""
    TOKEN = BOT_TOKEN
    text = (f"🆗🔔🆗 <b>Задание №{value['task_id']}</b> 🆗🔔🆗\n\n"
            f"🔸Задание было успешно выполнено. Все дни доставки были найдены.\n\n"
            f"Детали задания:\n"
            f"  🔹Склад: {value['warehouse_name']}.\n"
            f"  🔹Коэффициент: {value['task_coefficient']}.\n")
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
        "chat_id": value['telegram_id'],
        "text": text,
        "parse_mode": "HTML",
        "reply_markup": {
            "inline_keyboard": [[
                {
                    "text": "Убрать☠️",
                    "callback_data": "kill_myself"
                }
            ]]
        }
    }
    response_telegram = requests.post(url, json=data)
    if response_telegram.status_code == 200:
        print(f"Message sent to {value['telegram_id']}")
    else:
        print(f"Error sending message to {value['telegram_id']}")


def failed_task_handler(income_data: dict, warehouse_name: str) -> tuple:
    print('start filed message handler')
    TOKEN = BOT_TOKEN
    text = (
        f"❌🔔❌ <b>Не получилось №{income_data['id']}</b> ❌🔔❌\n\n"
        f"Слот склада с текущими параметрами задания не был найден.\n\n"
        f"Детали задания:\n"
        f"  Склад: {warehouse_name}.\n"
        f"  Коэффициент: {income_data['find_coefficient']} не был найден.\n"
    )
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": income_data['client'],
        "text": text,
        "parse_mode": "HTML",
        "reply_markup": {
            "inline_keyboard": [[
                {
                    "text": "Убрать☠️",
                    "callback_data": "kill_myself"
                }
            ]]
        }
    }
    response_telegram = requests.post(url, json=data)
    if response_telegram.status_code == 200:
        print(f"Message sent to {income_data['client']}")
    else:
        print(f"Error sending message to {income_data['client']}")
    response_django = requests.delete(U.URL_TASK + f"{income_data['id']}/?client={income_data['client']}")
    if response_django.status_code == 204:
        print(f"Task {income_data['id']} deleted")
    else:
        print(f"Error deleting task {income_data['id']}")
    return response_telegram, response_django
