from django.db.models import Count
from django.utils import timezone
from import_export.resources import Resource
from tablib import Dataset
from lottery.models import LotterySellers, LotteryClients
from bot.models import Seller,Client

class ClientsResourceWin(Resource):
    class Meta:
        fields = ('Покупатели',)

    def export(self, queryset=None, *args, **kwargs):
        dataset = Dataset()
        dataset.headers = self.get_export_headers()
        lottery_clients = LotteryClients.objects.last()

        if lottery_clients:
            clients = (
                Client.objects
                .filter(lottery_winner=lottery_clients)
                .prefetch_related('clientprofile', 'battery_cli')
                .annotate(total_batteries=Count('battery_cli'))
            )

        if not lottery_clients:
            dataset.append(['Розыгрыш не проводился','Добавьте розыгрыш'])
            return dataset


        dataset.append(['Тип участника','Telegram ID','Победитель','Тип приза','Имя','Фамилия','Отчество',
                        'Телефон','Email','Язык','Название компании','Адрес компании','Количество батарей'])


        if clients:
            for client in clients:
                dataset.append(['Покупатель',
                                client.user_telegram.telegram_id,
                                client.lottery_winner,
                                client.present_type,
                                client.clientprofile.first_name,
                                client.clientprofile.second_name,
                                client.clientprofile.patronymic,
                                client.clientprofile.contact_phone,
                                client.clientprofile.contact_email,
                                client.clientprofile.language,"-","-",client.total_batteries])
        return dataset

    @classmethod
    def get_display_name(cls):
        time = timezone.now()
        return f"Результаты розыгрыша покупателей {time.strftime('%d.%m.%Y %H:%M')}"

    def get_export_filename(self, file_format):
        time = timezone.now().strftime('%d-%m-%Y_%H-%M')
        return f"Результаты_розыгрыша_покупателей_{time}.{file_format.get_extension()}"


class SellersResourceWin(Resource):
    class Meta:
        fields = ('Продавцы',)

    def export(self, queryset=None, *args, **kwargs):
        dataset = Dataset()
        dataset.headers = self.get_export_headers()
        lottery_sellers = LotterySellers.objects.last()

        if lottery_sellers:
            sellers = (
                Seller.objects
                .filter(lottery_winner=lottery_sellers)
                .prefetch_related('sellerprofile', 'battery')
                .annotate(total_batteries=Count('battery'))
            )

        if not lottery_sellers:
            dataset.append(['Розыгрыш не проводился', ])
            return dataset

        dataset.append(['Тип участника', 'Telegram ID', 'Победитель', 'Тип приза', 'Имя', 'Фамилия', 'Отчество',
                        'Телефон', 'Email', 'Язык', 'Название компании', 'Адрес компании', 'Количество батарей'])


        if sellers:
            for seller in sellers:
                dataset.append(['Продавец',
                                seller.user_telegram.telegram_id,
                                seller.lottery_winner,
                                seller.present_type,
                                seller.sellerprofile.first_name,
                                seller.sellerprofile.second_name,
                                seller.sellerprofile.patronymic,
                                seller.sellerprofile.contact_phone,
                                seller.sellerprofile.contact_email,
                                seller.sellerprofile.language,
                                seller.sellerprofile.company_name,
                                seller.sellerprofile.company_address,
                                seller.total_batteries
                                ])
        return dataset

    @classmethod
    def get_display_name(cls):
        time = timezone.now()
        return f"Результаты розыгрыша {time.strftime('%d.%m.%Y %H:%M')}"

    def get_export_filename(self, file_format):
        time = timezone.now().strftime('%d-%m-%Y_%H-%M')
        return f"Результаты розыгрыша_{time}.{file_format.get_extension()}"
