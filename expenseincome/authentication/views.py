from django.shortcuts import render
from rest_framework.generics import GenericAPIView, views
from .serializers import RegisterationSerializer, EmailVerificationSerializer, LoginSerializer, RequestPasswordResetEmailSerializer, SetNewPasswordSerializer, PasswordCheckTokenSerializer
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
# for password reset
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import send_mail
# password reset end
from .renderers import UserRenderer

class RegisterView(GenericAPIView):

    serializer_class = RegisterationSerializer
    renderer_classes = (UserRenderer, )

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
        serializer = self.serializer_class(data=request.data)
        
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            # Password Reset Email Verify
            current_site = get_current_site(request=request).domain
            relative_link = reverse('password-reset-confirm',kwargs={'uidb64': uidb64, 'token': token})
            abs_url = 'http://' + current_site + relative_link
            email_body = 'Hi,\n Use the link to reset your password \n' + abs_url
            data = {
                'email_body': email_body,
                'email_subject': 'Reset your password',
                'email_to': user.email
            }

            Util.send_email(data)
            return Response({'message': 'We have sent you a link to reset your password.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Email Doesn\'t exist.'}, status=status.HTTP_404_NOT_FOUND)

        
class PasswordTokenCheckAPI(GenericAPIView):
    serializer_class = PasswordCheckTokenSerializer

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'This is not valid, request for new one.'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            return Response({'error': 'This is not valid, request for new one.'}, status=status.HTTP_401_UNAUTHORIZED)

class SetNewPasswordAPIView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password Reset Success'},status=status.HTTP_200_OK)
        