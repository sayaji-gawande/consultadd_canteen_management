from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['user_id', 'name', 'role', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            user_id=validated_data['user_id'],
            name=validated_data['name'],
            role=validated_data['role'],
            password=validated_data['password']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(user_id=data['user_id'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid user ID or password")
        if not user.is_active:
            raise serializers.ValidationError("User is inactive")
        return user
