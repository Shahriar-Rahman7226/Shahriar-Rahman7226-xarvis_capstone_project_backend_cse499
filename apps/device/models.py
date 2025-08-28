from django.db import models
from abstract.base_model import CustomModel
from apps.users.models import *
from external.choice_tuple import DeviceType


class DeviceModel(CustomModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='user_device')
    device_name = models.CharField(max_length=100)
    imei_1 = models.CharField(max_length=20, null=True, blank=True, unique=True)
    imei_2 = models.CharField(max_length=20, null=True, blank=True, unique=True)  # For second SIM slot
    device_type = models.CharField(max_length=100, choices=DeviceType)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True) 
    os_version = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.device_name if self.device_name else ''} -- {self.user.email if self.user else ''}"

    class Meta:
        db_table = 'device_models'
        ordering = ['-created_at']