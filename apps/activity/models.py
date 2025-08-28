from django.db import models
from abstract.base_model import CustomModel
from apps.users.models import *
from external.choice_tuple import ActionType

class ActivityLogModel(CustomModel):
    user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, related_name='user_activity')
    device_info = models.CharField(max_length=255, null=True, blank=True)
    details = models.TextField(null=True, blank=True) #Extra details (Optional)

    def __str__(self):
        return f"{self.action_type if self.action_type else ''} -- {self.user.email if self.user else ''}"

    class Meta:
        db_table = 'activity_log_models'
        ordering = ['-created_at']