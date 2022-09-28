from rest_framework import serializers
from django.contrib.auth import get_user_model

from .exceptions import (
    NotSamePassword2Exception,
    ExistingUsernameException,
)

User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        min_length=5,
        max_length=20,
    )
    email = serializers.EmailField(
        max_length=30,
        required=False,
    )
    first_name = serializers.CharField(
        required=False
    )
    last_name = serializers.CharField(
        required=False
    )
    role = serializers.ChoiceField(
        User.ROLES,
        error_messages={
            'invalid_choice': f'please choose between {User.ROLES}.'
        }
    )
    password = serializers.CharField(
        min_length=5,
        max_length=20
    )
    password2 = serializers.CharField(
        min_length=5,
        max_length=20
    )

    def validate_username(self, username):
        existing_username_list = User.objects.all().values_list('username', flat=True)
        if username in existing_username_list:
            raise serializers.ValidationError(ExistingUsernameException())
        return username

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': [NotSamePassword2Exception()]})
        return data

    def create(self, validated_data):
        user_info = {
            field: validated_data.get(field) for field in (
                'username',
                'email',
                'first_name',
                'last_name',
                'role',
            ) if validated_data.get(field) is not None
        }
        user = User.objects.create(**user_info)
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
        )

