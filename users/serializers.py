from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=2, max_length=50)
    password = serializers.CharField(min_length=6, max_length=128)
    

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists')
        return username

class UserAunthenticationSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=2, max_length=50, required=True)
    password = serializers.CharField(min_length=6, max_length=128, required=True)


class UserConfirmationSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField(max_length=6, min_length=6)