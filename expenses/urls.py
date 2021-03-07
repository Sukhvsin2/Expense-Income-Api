from django.urls import path
from .views import *

urlpatterns = [
    path('', ExpensesListAPIView.as_view(), name='ExpensesListAPIView'),
    path('<int:id>', ExpensesDetailAPIView.as_view(), name='ExpensesDetailAPIView'),
]
