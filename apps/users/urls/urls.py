from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users.views.views import *
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register('admin-registration', AdminResgistrationViewSet, basename='admin_registration')

urlpatterns = [
                  path(r'', include(router.urls)),
                  path('create-user/', UserResgistrationViewSet.as_view({'post': 'create_user'})),
              ] 