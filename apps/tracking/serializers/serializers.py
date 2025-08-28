from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.tracking.models import *

exclude_list = [
    'is_active',
    'created_at',
    'updated_at'
]

class LocationSerializer(ModelSerializer):
    
    class Meta:
        model = LocationModel
        exclude = exclude_list + ['id']