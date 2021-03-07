from rest_framework import serializers
from .models import Income

class IncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Income
        fields = ['date', 'id', 'amount', 'source', 'description']