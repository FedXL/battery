from rest_framework import serializers
from bot.models import Task, TaskDate
from parser.models import Warehouse


class ClientSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField(required=True)
    first_name = serializers.CharField(required=False)
    second_name = serializers.CharField(required=False)
    username = serializers.CharField(required=False)


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class DateChoiceSerializer(serializers.Serializer):
    data_choice = serializers.CharField(required=True)


class DeliveryTypeApiSerializer(serializers.Serializer):
    warehouse_id = serializers.CharField(required=True)


class TaskDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskDate
        fields = ['id', 'search_day']


class TaskSerializer(serializers.ModelSerializer):
    days = TaskDateSerializer(many=True)
    description = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'client', "description", 'warehouse', 'find_coefficient', 'delivery_type', 'days']

    def get_description(self, obj):
        return "Задание для будильника"

    def create(self, validated_data):
        days = validated_data.pop('days')
        task = Task.objects.create(**validated_data)
        for da in days:
            TaskDate.objects.create(task=task, **da)
        return task
