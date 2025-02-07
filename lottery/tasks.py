import io
from celery import shared_task
from PIL import Image, UnidentifiedImageError
from django.core.files.base import ContentFile
from django.db import transaction
from django.db.models import Count
from bot.bot_core.bot_core import sync_bot
from bot.models import Client, Seller
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
def clients_lottery_start(lottey_id: int):
    lottery = LotteryClients.objects.get(id=lottey_id)
    little_count = lottery.little_prize
    big_count = lottery.big_prize
    try:
        clients = (
            Client.objects.filter(lottery_winner=None)  # SQL: WHERE lottery_winner IS NULL
            .annotate(num_batteries=Count('battery'))  # SQL: COUNT(battery.id) GROUP BY client.id
            .filter(num_batteries__gt=0)  # SQL: HAVING COUNT(battery.id) > 0
            .prefetch_related('battery_set')
        )

        clients_count = clients.count()
        clients_dict = {num:client for num, client in enumerate(clients, start=1)}
        big_winners, little_winners = get_random_winners(clients_count=clients_count,
                                                       winners_little_count=little_count,
                                                       winners_big_count=big_count)
        my_logger.info(f"clients_count: {clients_count}")
        my_logger.info(f"big_winners: {big_winners}")
        my_logger.info(f"little_winners: {little_winners}")
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
            if big_winners:
                for winner1 in big_winners:
                    my_logger.info(f"winner1: {winner1}")
                    client = clients_dict[winner1]
                    client.lottery_winner = lottery
                    client.present_type = 'big'
                    client.save()
            if little_winners:
                for winner2 in little_winners:
                    my_logger.info(f"winner2: {winner2}")
                    client = clients_dict[winner2]
                    client.lottery_winner = lottery
                    client.present_type = 'little'
                    client.save()

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
        sellers=(
            Seller.objects.filter(lottery_winner=None)  # SQL: WHERE lottery_winner IS NULL
            .annotate(num_batteries=Count('battery'))  # SQL: COUNT(battery.id) GROUP BY client.id
            .filter(num_batteries__gt=0)  # SQL: HAVING COUNT(battery.id) > 0
            .prefetch_related('battery_set')
            .order_by('-num_batteries')
        )
        my_logger.info('Из скольких продавцов выбираем победителей')
        winners = sellers[:count_of_winners]
    except Exception as e:
        my_logger.error(f"Ошибка при выборе победителей: {e}")
        lottery.report = f"Ошибка при формировании списка победителей: {e}"
        return 'FAIL'
    try:
        with transaction.atomic():
            for num, winner in enumerate(winners, start=1):
                winner.lottery_winner = lottery
                winner.present_type = 'little'
                winner.save()
        lottery.report = 'Статус: Успешно'
        lottery.save()
        return 'OK'
    except Exception as e:
        my_logger.error(f"Ошибка при сохранении победителей: {e}")
        lottery.report = f"Ошибка при сохранении результатов : {e}"
        lottery.save()
        return "FAIL"






























