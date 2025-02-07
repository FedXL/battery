from django.db.models.signals import post_delete
from django.dispatch import receiver

from bot.models import Client, Seller
from logs.my_logger import my_logger
from lottery.models import LotteryClients, LotterySellers


@receiver(post_delete, sender=LotteryClients)
def clean_clients(sender, instance, **kwargs):
    my_logger.info(f"SIGNAL from LotteryClients: {instance}")
    clients1 = Client.objects.filter(lottery_winner=None).exclude(present_type=None)
    clients1.update(present_type=None)
    clients2 = Client.objects.filter(lottery_winner=instance)
    clients2.update(present_type=None)



@receiver(post_delete, sender=LotterySellers)
def clean_sellers(sender,instance,**kwargs):
    my_logger.info(f"SIGNAL from LotterySellers: {instance}")
    sellers1 = Seller.objects.filter(lottery_winner=None).exclude(present_type=None)
    sellers1.update(present_type=None)
    sellers2 = Seller.objects.filter(lottery_winner=instance)
    sellers2.update(present_type=None)
