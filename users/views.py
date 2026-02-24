from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserAunthenticationSerializer, UserConfirmationSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random
from .models import UserConfirmation
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model

User = get_user_model()

@swagger_auto_schema(methods=['post'], request_body=UserRegistrationSerializer)
@api_view(['POST'])
def registration_api_view(request):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    phone = serializer.validated_data.get('phone_number', None)
    user = User.objects.create_user(email=email, password=password, phone_number=phone, is_active=False)
    generated_code = str(random.randint(100000, 999999))
    UserConfirmation.objects.create(user=user, code=generated_code)
    return Response(status=status.HTTP_201_CREATED, data={'id': user.id, 'email':user.email, 'code':generated_code})


@api_view(['POST'])
def confirmation_api_view(request):
    serializer = UserConfirmationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    code = serializer.validated_data['code']
    try:
        user = User.objects.get(email=email)
        confirmation = UserConfirmation.objects.get(user=user)
        if  confirmation.code == code:
            user.is_active = True
            user.save()
            confirmation.delete()
            return Response(status=status.HTTP_200_OK, data={'message': 'User confirmed successfully'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Invalid confirmation code'})
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'User not found'})
    except UserConfirmation.DoesNotExist: 
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Confirmation not found'})

@swagger_auto_schema(methods=['post'],request_body=UserAunthenticationSerializer)
@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserAunthenticationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    user = authenticate(email=email, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response(status=status.HTTP_200_OK, data={'token': token.key})
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={'error': 'Invalid email or password'})

    