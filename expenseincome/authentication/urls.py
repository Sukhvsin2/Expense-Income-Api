from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView
)

urlpatterns = [
    path('login', LoginView.as_view(), name='LoginView'),
    path('register/', RegisterView.as_view(), name='RegisterView'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='tokenRefresh'),
    path('request-reset-email', RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/token/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
]
