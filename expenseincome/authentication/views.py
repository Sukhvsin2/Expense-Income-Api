from django.shortcuts import render
from rest_framework.generics import GenericAPIView, views
from .serializers import RegisterationSerializer, EmailVerificationSerializer, LoginSerializer, RequestPasswordResetEmailSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
import os
from dotenv import load_dotenv
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RegisterView(GenericAPIView):

    serializer_class = RegisterationSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token

        # verifying by email
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        abs_url = 'http://' + current_site + relative_link + "?token=" + str(token)
        email_body = 'Hi! ' + user.username + ' Use the link to verify your email \n' + abs_url
        data = {
            'email_body': email_body,
            'email_subject': 'Verify your Email',
            'email_to': user.email
        }

        Util.send_email(data)

        return Response(data=user_data, status=status.HTTP_201_CREATED)

class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        print('token ', token)
        key = str(os.getenv('SECRET_KEY'))
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            print('payload check ',payload)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'message': 'Account Verified'}, status=status.HTTP_202_ACCEPTED)
            
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Link is expired'}, status=status.HTTP_400_BAD_REQUEST)
            
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RequestPasswordResetEmail(GenericAPIView):
    serializer_class = RequestPasswordResetEmailSerializer

    def post(self, request):
        data = {'request': request, 'data': request.data}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'We have sent you a link to reset your password.'}, status=status.HTTP_200_OK)
        
class PasswordTokenCheckAPI(GenericAPIView):

    def get(self, request, uidb64, token):
        pass
