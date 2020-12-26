from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import RegisterationSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
import os

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

class VerifyEmail(GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        key = os.getenv('KEY')
        try:
            payload = jwt.decode(token, key)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'message': 'Account Verified'}, status=status.HTTP_202_ACCEPTED)
            
        except jwt.ExpiredSignature as identifier:
            return Response({'error': 'Link is expired'}, status=status.HTTP_400_BAD_REQUEST)
            
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)