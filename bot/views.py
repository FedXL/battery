from datetime import timedelta
from babel.dates import format_date
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from bot.management.bot_core.handlers.bot_utils.bot_variables import CRITERIA_WORD
from bot.serializers import ClientSerializer, WarehouseSerializer, DateChoiceSerializer, DeliveryTypeApiSerializer, \
    TaskSerializer, TaskDateSerializer


# class CreateClientApiView(APIView):
#     def post(self, request):
#         serializer = ClientSerializer(data=request.data)
#         if serializer.is_valid():
#             client, created = Client.objects.update_or_create(
#                 telegram_id=serializer.validated_data['telegram_id'],
#                 defaults=serializer.validated_data
#             )
#             if created:
#                 return Response(status=status.HTTP_201_CREATED)
#             else:
#                 return Response(status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class CustomPageNumberPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     max_page_size = 1000
#
#     def get_paginated_response(self, data):
#         return Response({
#             'links': {
#                 'next': self.get_next_link(),
#                 'previous': self.get_previous_link()
#             },
#             'current_page': self.page.number,
#             'total_pages': self.page.paginator.num_pages,
#             'total_items': self.page.paginator.count,
#             'page_size': self.get_page_size(self.request),
#             'results': data
#         })
#
#
# class WarehouseApiViewSet(ReadOnlyModelViewSet):
#     queryset = Warehouse.objects.all()
#     serializer_class = WarehouseSerializer
#     pagination_class = CustomPageNumberPagination
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         warehouse_collection = self.request.query_params.get('warehouse_collection_name')
#         if not warehouse_collection:
#             return queryset
#         elif warehouse_collection == 'SC':
#             criteria = "СЦ"
#             queryset = queryset.filter(name__icontains=criteria).order_by('name')
#         elif warehouse_collection == "MAIN":
#             criteria = "СЦ"
#             queryset = queryset.exclude(name__icontains=criteria).order_by('name')
#         elif warehouse_collection == "ALL":
#             return queryset
#         return queryset
#
#
# class DataChoiceApiView(APIView):
#     def post(self, request):
#         serializer = DateChoiceSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         result_date = {}
#         choose = serializer.validated_data.get('data_choice')
#         queryset = Date.objects.order_by('date')
#         first_date = queryset.first().date
#         last_date = queryset.last().date
#         result_date['first_date'] = first_date
#         result_date['last_date'] = last_date
#         if choose == 'custom':
#             result_date['dates_list'] = {}
#             available_dates = queryset.values_list('date', flat=True)
#             for row in available_dates:
#                 formatted_date = format_date(row, 'd MMM', locale='ru')
#                 result_date["dates_list"][formatted_date] = row
#         if choose == "this_week":
#             seventh_date = first_date + timedelta(days=6)
#             seventh_date_object = queryset.filter(date=seventh_date).first().date
#             result_date['last_date'] = seventh_date_object
#         return Response(result_date, status=status.HTTP_200_OK)
#
#
# class DeliveryTypeApiView(APIView):
#     def post(self, request):
#         serializer = DeliveryTypeApiSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         warehouse_id = serializer.validated_data['warehouse_id']
#         coefficients = (Coefficient.objects.
#                         filter(warehouse=warehouse_id).
#                         values_list('korobs',
#                                     'monopollet',
#                                     'supersafe',
#                                     'QR_send_korobs'))
#         result = {
#             'korobs': set(),
#             'monopolets': set(),
#             'supersafe': set(),
#             'QR_send_korobs': set(),
#         }
#         for korobs, monopollet, supersafe, QR_send_korobs in coefficients:
#             result['korobs'].add(korobs)
#             result['monopolets'].add(monopollet)
#             result['supersafe'].add(supersafe)
#             result['QR_send_korobs'].add(QR_send_korobs)
#
#         for key, value in result.items():
#             value.discard(99)
#             value.discard('99')
#
#         result = {key: value for key, value in result.items() if value}
#
#         result['warehouse_id'] = warehouse_id
#         result['warehouse_name'] = Warehouse.objects.get(id=warehouse_id).name
#
#         return Response(data=result, status=status.HTTP_200_OK)
#
#
# class TaskApiViewSet(ModelViewSet):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         client_id = self.request.query_params.get('client')
#         if not client_id:
#             return queryset
#         return queryset.filter(client_id=client_id)
#
#
# class TaskDayApiViewSet(ModelViewSet):
#     queryset = TaskDate.objects.all()
#     serializer_class = TaskDateSerializer
#