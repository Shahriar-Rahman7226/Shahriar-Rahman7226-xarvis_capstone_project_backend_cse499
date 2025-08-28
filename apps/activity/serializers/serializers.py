from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.activity.models import *

exclude_list = [
    'is_active',
    'created_at',
    'updated_at'
]

class ActivityLogCreateSerializer(ModelSerializer):
    action_type = serializers.ChoiceField(choices=ActionType)
    class Meta:
        model = ActivityLogModel
        exclude = exclude_list + ['id']

class ActivityLogListSerializer(ModelSerializer):
    class Meta:
        model = ActivityLogModel
        exclude = exclude_list