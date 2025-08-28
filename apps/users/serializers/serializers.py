from rest_framework import serializers
from rest_framework.serializers import *
from apps.users.models import *

exclude_list = [
    'is_active',
    'created_at',
    'updated_at'
]


class UserCreateSerializer(ModelSerializer):
    password = CharField(max_length=128, allow_blank=False, allow_null=False)
    user_role = serializers.ChoiceField(choices=UserRole)
    
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password', 'user_role']

class UserUpdateSerializer(ModelSerializer):
    
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'email', 'phone_number']


class UserListSerializer(ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        exclude = [
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login',
            'created_at',
            'updated_at',
            'login_attempt',
            'user_permissions',
            'groups',
            'two_factor',
            'first_name',
            'last_name',
            'password',
        ]
    
    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
