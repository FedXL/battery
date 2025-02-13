import io
import random

from celery import shared_task
from PIL import Image, UnidentifiedImageError
from django.core.files.base import ContentFile
from django.db import transaction
from django.db.models import Count
from bot.bot_core.bot_core import sync_bot
from bot.bot_core.collections.variables import Templates
from bot.models import Client, Seller
from bot.tasks import send_message
from logs.my_logger import my_logger
from lottery.models import Battery, InvoicePhoto, LotteryClients, LotterySellers
from lottery.utils import get_random_winners

@shared_task
def extract_invoice(battery_id: int) -> None:
    try:
        battery = Battery.objects.get(id=battery_id)
        file_id = battery.invoice_telegram_id
        if not file_id:
            return 'No invoice photo'

        file, comment = sync_bot.extract_photo_by_id(file_id)
        if not file:
            print(f"[ERROR] extract bot error: {comment}")
            return
        image = Image.open(io.BytesIO(file))
        image_format = image.format.lower()
        image_io = io.BytesIO()

        image.save(image_io, format=image_format.upper())
        image_io.seek(0)

        invoice_photo = InvoicePhoto(battery=battery)
        invoice_photo.photo.save(f"{battery.id}.{image_format}", ContentFile(image_io.read()), save=True)

        print(f"[INFO] Файл успешно загружен в ImageField: {invoice_photo.photo.url}")

    except Battery.DoesNotExist:
        print(f"[ERROR] Battery {battery_id} not found")
    except UnidentifiedImageError:
        print(f"[ERROR] Файл {file_id} не является допустимым изображением!")
    except Exception as e:
        print(f"[CRITICAL] extract_invoice error: {str(e)}")



@shared_task
def clients_lottery_start(lottery_id: int):
    lottery = LotteryClients.objects.get(id=lottery_id)
    little_count = lottery.little_prize
    big_count = lottery.big_prize
    super_prize = lottery.super_prize

    try:
        clients = (
            Client.objects.filter(lottery_winner=None)
            .annotate(num_batteries=Count('battery_cli'))
            .filter(num_batteries__gt=0)
            .prefetch_related('battery_cli')
        )
        clients_count = clients.count()
        clients_dict = {num: client for num, client in enumerate(clients, start=1)}
    except Exception as e:
        my_logger.error(f"Ошибка при выборе победителей: {e}")
        lottery.report = f"Ошибка при выборке списка победителей: {e}"
        return 'FAIL'

    try:
        if not super_prize:
            big_winners, little_winners = get_random_winners(
                clients_count=clients_count,
                winners_little_count=little_count,
                winners_big_count=big_count
            )
            report = (f"Статус: Успешно\n"
                      f"Розыгрыш {lottery.name}\n"
                      f"Призов разыграно 25000: {little_count}\n"
                      f"Призов разыграно 50000: {big_count}\n")
    except Exception as e:
        my_logger.error(f"Ошибка при выборе победителей: {e}")
        report = f"Ошибка при формировании списка победителей: {e}"
        lottery.report = report
        lottery.save()
        return 'FAIL'

    try:
        with transaction.atomic():
            if super_prize:
                super_winner = random.randint(1, clients_count)
                super_client = clients_dict[super_winner]
                super_client.lottery_winner = lottery
                super_client.present_type = '1000000'
                super_client.save()
                report = (f"Статус: Успешно\n"
                          f"Розыгрыш {lottery.name}\n"
                          f"Призов разыграно 1000000: 1\n")
            else:
                winners = []
                for winner_id in big_winners:
                    client = clients_dict[winner_id]
                    client.lottery_winner = lottery
                    client.present_type = '50000'
                    winners.append(client)

                for winner_id in little_winners:
                    client = clients_dict[winner_id]
                    client.lottery_winner = lottery
                    client.present_type = '25000'
                    winners.append(client)

                Client.objects.bulk_update(winners, ['lottery_winner', 'present_type'])
    except Exception as e:
        my_logger.error(f"Ошибка при сохранении победителей: {e}")
        report = f"Ошибка при сохранении результатов: {e}"
        lottery.report = report
        lottery.save()
        return "FAIL"

    lottery.report = report
    lottery.save()
    return 'OK'


@shared_task
def sellers_lottery_start(lottey_id: int):
    lottery = LotterySellers.objects.get(id=lottey_id)
    count_of_winners = lottery.little_prize
    try:
        sellers = (
            Seller.objects.filter(lottery_winner=None)  # WHERE lottery_winner IS NULL
            .annotate(num_batteries=Count('battery'))  # COUNT(battery.id) GROUP BY seller.id
            .filter(num_batteries__gt=0)  # HAVING COUNT(battery.id) > 0
            .prefetch_related('battery')
            .order_by('-num_batteries')
        )
        my_logger.info(f'Из скольких продавцов выбираем победителей: {sellers.count()}')
        winners = list(sellers[:count_of_winners])
    except Exception as e:
        my_logger.error(f"Ошибка при выборе победителей: {e}")
        lottery.report = f"Ошибка при формировании списка победителей: {e}"
        lottery.save()
        return 'FAIL'

    try:
        with transaction.atomic():
            for winner in winners:
                winner.lottery_winner = lottery
                winner.present_type = '25000'

            Seller.objects.bulk_update(winners, ['lottery_winner', 'present_type'])

        lottery.report = 'Статус: Успешно'
        lottery.save()
        return 'OK'
    except Exception as e:
        my_logger.error(f"Ошибка при сохранении победителей: {e}")
        lottery.report = f"Ошибка при сохранении результатов: {e}"
        lottery.save()
        return "FAIL"


@shared_task
def check_for_extract_invoices():
    batteries = Battery.objects.filter(invoice_photo__isnull=True).exclude(invoice_telegram_id="")
    for battery in batteries:
        extract_invoice.delay(battery.id)
    return 'OK'

@shared_task
def send_notification_to_clients(lottery_id):
    lottery = LotteryClients.objects.get(id=lottery_id)
    clients_25 = Client.objects.filter(lottery_winner=lottery, present_type='25000')
    clients_50 = Client.objects.filter(lottery_winner=lottery, present_type='50000')
    for client in clients_25:
        send_message.delay(client.user_telegram.telegram_id, Templates.client_win_25000)
    for client in clients_50:
        send_message.delay(client.user_telegram.telegram_id, Templates.client_win_50000)
    return 'OK'

@shared_task
def send_notification_to_sellers(lottery_id):
    lottery = LotterySellers.objects.get(id=lottery_id)
    sellers_25 = Seller.objects.filter(lottery_winner=lottery,present_type='25000')
    for seller in sellers_25:
        send_message.delay(seller.user_telegram.telegram_id, Templates.seller_win_25000)
    return 'OK'




























