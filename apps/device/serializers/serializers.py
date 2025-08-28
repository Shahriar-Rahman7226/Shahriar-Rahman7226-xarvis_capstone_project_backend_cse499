from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.device.models import *

exclude_list = [
    'is_active',
    'created_at',
    'updated_at'
]

class DeviceCreateSerializer(ModelSerializer):
    device_type = serializers.ChoiceField(choices=DeviceType)
    class Meta:
        model = DeviceModel
        exclude = exclude_list + ['id']

class DeviceUpdateSerializer(ModelSerializer):
    device_type = serializers.ChoiceField(choices=DeviceType)
    class Meta:
        model = UserModel
        fields = ['device_name', 'imei_1', 'imei_2', 'device_type', 'phone_number', 'os_version']

class DeviceListSerializer(ModelSerializer):
    class Meta:
        model = DeviceModel
        exclude = exclude_list

class DeviceSerializer(ModelSerializer):
    class Meta:
        model = DeviceModel
        exclude = exclude_list + ['id']