from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from external.pagination import CustomPagination
from external.swagger_query_params import set_query_params
from apps.users.serializers.serializers import *
from apps.users.models import *
from external.send_message import send_email
from rest_framework import status
from external.permission_decorator import allowed_users
from external.query_helper import get_query_data
from apps.activity.serializers.serializers import ActivityLogCreateSerializer

@extend_schema(tags=['Admin Registration'])
class AdminResgistrationViewSet(ModelViewSet):
    model_class = UserModel
    serializer_class = UserCreateSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UserListSerializer
        elif self.action =='update':
            return UserUpdateSerializer
        return self.serializer_class

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Admin",
                value={
                    "first_name": "string",
                    "last_name": "string",
                    "email": "string",
                    "password": "string",
                    "phone_number": "string",
                },
                request_only=True,
            )
        ]
    )
    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        queryset = self.queryset
        data = request.data
        if queryset.filter(email=data['email']).first():
            return Response({'message': 'Email is already in use.'}, status=status.HTTP_400_)

        if queryset.filter(phone_number=data['phone_number']).first():
            return Response({'message': 'Phone number is already in use.'}, status=status.HTTP_400_BAD_REQUEST)

        if 'password' in data.keys():
            try:
                validate_password(data['password'])
                data['password'] = make_password(data['password'])
            except ValidationError:
                return Response({'message': 'Given password is too weak.'}, status=status.HTTP_400_BAD_REQUEST)
        data['user_role'] = UserRole[0][0]

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            user_obj = serializer.save()
            subject = 'XARVIS'
            message = "Welcome to XARVIS - your device's new personal bodyguard. \n With every feature at your fingertips, your phone is now one step ahead of threats."
            send_email(user_obj.id, subject, message, None)
            return Response({'message': 'Admin created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    @extend_schema(
        examples=[
            OpenApiExample(
                "Update User",
                value={
                    "first_name": "string",
                    "last_name": "string",
                    "email": "user@example.com",
                    "phone_number": "string",
                },
                request_only=True,
            )
        ],
    )
    @transaction.atomic()
    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.queryset.filter(id=request.user.id).first()

        if not instance:
            return Response({'message': 'User does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        if 'email' in data.keys():
            if self.model_class.objects.filter(email=data['email']).first():
                return Response({'message': 'Email is already in use.'}, status=status.HTTP_400_BAD_REQUEST)

        if 'phone_number' in data.keys():
            if self.model_class.objects.filter(phone_number=data['phone_number']).first():
                return Response({'message': 'Phone number is already in use.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            subject = 'XARVIS'
            message = 'Your profile information was updated successfully.'
            send_email(None, subject, message, request.user.id)
            # send_sms()
            return Response({'message': 'User updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(parameters=set_query_params('list', [
        {"name": 'first_name', "description": 'Filter by first_name'},
    ]))
    @allowed_users(allowed_roles=['ADMIN'])
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        params = request.query_params
        if params:
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
        obj = queryset.filter(id=request.user.id).first()
        if not obj:
            return Response({'message': 'User does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['User Registration'])
class UserResgistrationViewSet(ModelViewSet):
    model_class = UserModel
    serializer_class = UserCreateSerializer
    queryset = model_class.objects.all()
    permission_classes = []
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create User",
                value={
                    "first_name": "string",
                    "last_name": "string",
                    "email": "string",
                    "password": "string",
                    "phone_number": "string",
                },
                request_only=True,
            )
        ]
    )
    @transaction.atomic()
    def create_user(self, request, *args, **kwargs):
        queryset = self.queryset
        data = request.data
        if queryset.filter(email=data['email']).first():
            return Response({'message': 'Email is already in use.'}, status=status.HTTP_400_)

        if queryset.filter(phone_number=data['phone_number']).first():
            return Response({'message': 'Phone number is already in use.'}, status=status.HTTP_400_BAD_REQUEST)

        if 'password' in data.keys():
            try:
                validate_password(data['password'])
                data['password'] = make_password(data['password'])
            except ValidationError:
                return Response({'message': 'Given password is too weak.'}, status=status.HTTP_400_BAD_REQUEST)
        data['user_role'] = UserRole[1][0]
        
        serializer_class = self.serializer_class
        serializer = serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            user_obj = serializer.save()

            subject = 'XARVIS'
            message = "Welcome to XARVIS - your device’s new personal bodyguard. \n With every feature at your fingertips, your phone is now one step ahead of threats."
            send_email(user_obj.id, subject, message, None)
            # send_sms()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    