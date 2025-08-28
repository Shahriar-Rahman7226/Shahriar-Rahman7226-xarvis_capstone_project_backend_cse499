from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.device.views.views import DeviceViewSet
from apps.tracking.views.views import LocationViewSet 

router = DefaultRouter()
router.register('device', DeviceViewSet, basename='device')
router.register('location', LocationViewSet, basename='location')  

urlpatterns = [
    path('', include(router.urls)),
    path('get-device/', DeviceViewSet.as_view({'get': 'get_device'})),
    path('location/<int:pk>/last-locations/', LocationViewSet.as_view({'get': 'last_locations'}), name='last-locations'),
]
