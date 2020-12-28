from django.urls import path
from .views import ExpenseSummaryStats

urlpatterns = [
    path('expenses_category_data', ExpenseSummaryStats.as_view(), name='expense-summary-stats'),
]
