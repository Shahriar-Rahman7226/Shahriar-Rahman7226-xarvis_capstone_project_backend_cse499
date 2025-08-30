from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.device.views.views import DeviceViewSet
from apps.tracking.views.views import LocationViewSet 

router = DefaultRouter()
router.register('location', LocationViewSet, basename='location')  

urlpatterns = [
    path('', include(router.urls)),
    path('location/get-next-location/', LocationViewSet.as_view({'get': 'get_next_location'}), name='get-next-location'),
]
