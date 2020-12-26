from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

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