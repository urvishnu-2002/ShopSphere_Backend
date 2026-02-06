from rest_framework import serializers
from .models import AuthUser


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = AuthUser.objects.create_user(**validated_data)
        return user
