from django.urls import path
from .views import *

urlpatterns = [
    path('', IncomeListAPIView.as_view(), name='IncomeListsAPIView'),
    path('<int:id>', IncomeDetailAPIView.as_view(), name='IncomeDetailsAPIView'),
]
