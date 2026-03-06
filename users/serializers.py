from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, max_length=128)
    phone_number = serializers.CharField(max_length=15, required=False)
    birth_date = serializers.DateField(required=False)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already exists')
        return email

class UserAunthenticationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, max_length=128, required=True)

class UserConfirmationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6, min_length=6)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['birth_date'] = user.birth_date
        return token
    
class OauthCodeSerializer(serializers.Serializer):
    code = serializers.CharField()