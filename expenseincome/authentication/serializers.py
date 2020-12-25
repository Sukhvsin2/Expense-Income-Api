from rest_framework import serializers
from .models import User

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

