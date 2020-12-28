from rest_framework import serializers
from authentication.models import User

class ExpenseStatsSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555, write_only=True)

    class Meta:
        model = User
        fields = ['token']
