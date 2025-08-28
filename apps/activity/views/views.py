from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from external.pagination import CustomPagination
from external.swagger_query_params import set_query_params
from apps.activity.models import *
from apps.activity.serializers.serializers import *
from django.db import transaction
from rest_framework import status
from external.query_helper import get_query_data

@extend_schema(tags=['Activity Log'])
class ActivityLogViewSet(ModelViewSet):
    model_class = ActivityLogModel
    serializer_class = ActivityLogListSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action == 'create':
            return ActivityLogCreateSerializer
        return self.serializer_class
    
    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Activity",
                value={
                    "user": "string",
                    "action_type": "string",
                    "device_info": "string",
                    "details": "string",
                },
                request_only=True,
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Activity added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(parameters=set_query_params('list', [
        {"name": 'user', "description": 'Filter by user Id'},
        {"name": 'action_type', "description": 'Filter by action_type'},
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


    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=kwargs['id']).first()
        if not obj:
            return Response({'message': 'Invalid activity'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)