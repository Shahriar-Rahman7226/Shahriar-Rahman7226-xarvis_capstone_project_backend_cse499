from django.db import models
from abstract.base_model import CustomModel
from apps.users.models import *
from apps.device.models import *


class LocationModel(CustomModel):
    device = models.ForeignKey(DeviceModel, on_delete=models.CASCADE, related_name='device_location', null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    thana = models.CharField(max_length=100, null=True, blank=True) # locality
    district = models.CharField(max_length=100, null=True, blank=True)  
    accuracy = models.FloatField(null=True, blank=True) # From 1 to 10
    signal_strength = models.FloatField(null=True, blank=True, help_text="Signal strength in dBm")
    network_type = models.CharField(max_length=50, null=True, blank=True, help_text="Type of network (e.g., 4G, WiFi)")  
   
    def __str__(self):
        return f"{self.thana if self.thana else ''} -- {self.device.device_id if self.device else ''}"

    class Meta:
        db_table = 'location_models'
        ordering = ['-created_at']
    


