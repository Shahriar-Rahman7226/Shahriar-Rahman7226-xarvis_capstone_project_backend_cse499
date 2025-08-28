from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from external.pagination import CustomPagination
from external.swagger_query_params import set_query_params
from apps.device.models import *
from apps.device.serializers.serializers import *
from django.db import transaction
from rest_framework import status
from external.query_helper import get_query_data

@extend_schema(tags=['Device'])
class DeviceViewSet(ModelViewSet):
    model_class = DeviceModel
    serializer_class = DeviceListSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action == 'create':
            return DeviceCreateSerializer
        elif self.action == 'update':
            return self.serializer_class
    
    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Device",
                value={
                    "user": "string",
                    "device_name": "string",
                    "imei_1": "string",
                    "imei_2": "string",
                    "device_type": "string",
                    "phone_number": "string",
                    "os_version": "string",
                },
                request_only=True,
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        data=request.data
        data['user']=request.user.id
        serializer = serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Device added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        examples=[
            OpenApiExample(
                "Update Device",
                value={
                    "user": "string",
                    "device_name": "string",
                    "imei_1": "string",
                    "imei_2": "string",
                    "device_type": "string",
                    "phone_number": "string",
                    "os_version": "string",
                },
                request_only=True,
            )
        ]
    )
    def update(self, request, *args, **kwargs):
        instance = self.model_class.objects.filter(id=kwargs['id']).first()
        if not instance:
            return Response({'message': 'Invalid device'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Device information updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(parameters=set_query_params('list', [
        {"name": 'user', "description": 'Filter by user Id'},
    ]))
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        params = request.query_params.copy()

        queryset=get_query_data(params, queryset)
        page = self.paginate_queryset(queryset)
        serializer_class = self.get_serializer_class()
        if page is not None:
            serializer = serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    # def retrieve(self, request, *args, **kwargs):
    #     queryset = self.queryset
    #     obj = queryset.filter(id=kwargs['id']).first()
    #     if not obj:
    #         return Response({'message': 'Invalid device'}, status=status.HTTP_400_BAD_REQUEST)
    #     serializer_class = self.get_serializer_class()
    #     serializer = serializer_class(obj)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def get_device(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(user=request.user.id).first()
        if not obj:
            return Response({'message': 'Invalid device'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)