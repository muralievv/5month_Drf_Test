from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    #TokenObtainPairView,
    TokenRefreshView,
)
from .views import CustomTokenObtainPairView

urlpatterns = [
    path('registration/', views.registration_api_view),
    path('confirmation/', views.confirmation_api_view),
    path('authorization/', views.authorization_api_view),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]