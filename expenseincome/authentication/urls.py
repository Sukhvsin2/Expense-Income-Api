from django.urls import path
from .views import *

urlpatterns = [
    path('login', LoginView.as_view(), name='LoginView'),
    path('register/', RegisterView.as_view(), name='RegisterView'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
]
