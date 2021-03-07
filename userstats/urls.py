from django.urls import path
from .views import ExpenseSummaryStats, IncomeSummaryStats

urlpatterns = [
    path('expenses_category_data', ExpenseSummaryStats.as_view(), name='expense-summary-stats'),
    path('income_category_data', IncomeSummaryStats.as_view(), name='income-summary-stats'),
]
