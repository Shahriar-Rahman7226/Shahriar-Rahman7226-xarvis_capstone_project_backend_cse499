from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.activity.views.views import *

router = DefaultRouter()
router.register('activity', ActivityLogViewSet, basename='activity')

urlpatterns = [
                  path(r'', include(router.urls)),
              ] 