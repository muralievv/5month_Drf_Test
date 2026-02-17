from django.urls import path, include
from . import views

urlpatterns = [
    path('registration/', views.registration_api_view),
    path('confirmation/', views.confirmation_api_view),
    path('authorization/', views.authorization_api_view),
]