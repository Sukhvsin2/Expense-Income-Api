from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import *
from .models import Income
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner

class IncomeListAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = IncomeSerializer
    queryset = Income.objects.all()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
class IncomeDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwner,)

    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    