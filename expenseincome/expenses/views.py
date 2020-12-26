from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import *
from .models import Expenses
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner

class ExpensesListAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = ExpenseSerializer
    queryset = Expenses.objects.all()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
class ExpensesDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwner,)

    serializer_class = ExpenseSerializer
    queryset = Expenses.objects.all()
    lookup_field = 'id'

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    