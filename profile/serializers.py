from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.hashers import make_password

class RegisterSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(
            password=validated_data['password'],
            username=validated_data['username'],
            email=validated_data['email']
        )
        return user

    def update(self, instance, validated_data):
        if 'username' in validated_data:
            instance.user.password = make_password(
                validated_data.get('username').get('password', instance.user.password)
            )
            instance.user.save()

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "email",
        ]

class ProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='get_username', read_only=True)
    email = serializers.CharField(source='get_user_email', read_only=True)

    class Meta:
        model = Profile
        fields = [
            "name",
            "surname",
            "created",
            "username",
            "email"
        ]