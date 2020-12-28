from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode



class RegisterationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    #  This would be called when is_valid() execute
    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username','')

        if not username.isalnum():
            raise serializers.ValidationError('Username can\'t have special character!')

        return attrs

    # This would be called when save() execute
    def create(self, validated_data):
        # ** to pass all data in it.
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    
    class Meta:
        model = User
        fields = ['token']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=68, write_only=True)
    username = serializers.CharField(max_length=255, read_only=True)
    tokens = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']
    
    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        
        user = auth.authenticate(email=email, password=password)
        
        if not user:
            raise AuthenticationFailed('Invalid Credentials try again!')
        
        if not user.is_active:
            raise AuthenticationFailed('Account not active, contact Admin')


        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

class RequestPasswordResetEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        model = User
        fields = ['email']

class SetNewPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    token = serializers.CharField(min_length=2, write_only=True)
    uidb64 = serializers.CharField(min_length=2, write_only=True)
    
    class Meta:
        model = User
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            
            user.set_password(password)
            user.save()
            return user

        except DjangoUnicodeDecodeError as identifier:
            raise AuthenticationFailed('The reset link is invalid', 401)

        return super.validate(attrs)


class PasswordCheckTokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555, write_only=True)
    uidb64 = serializers.CharField(max_length=64, write_only=True)

    class Meta:
        model = User
        fields = ['uidb64', 'token']