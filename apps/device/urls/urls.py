from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.device.views.views import *

router = DefaultRouter()
router.register('device', DeviceViewSet, basename='device')

urlpatterns = [
                  path(r'', include(router.urls)),
                  path('get-device/', DeviceViewSet.as_view({'get': 'get_device'})),
              ] 