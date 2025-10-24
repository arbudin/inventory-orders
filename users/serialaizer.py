from rest_framework import serializers
from django.contrib.auth.models import User

from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового """
    password = serializers.CharField(
        min_length=6,
        write_only=True)

    # поля для считывания сериализатором
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get('username') or validated_data['email'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

