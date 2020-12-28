from rest_framework.views import APIView
import datetime
from expenses.models import Expenses
from income.models import Income
from rest_framework.response import Response
from rest_framework import status
from .serializers import ExpenseStatsSerializer
from rest_framework.permissions import IsAuthenticated
from .permission import IsOwner

class ExpenseSummaryStats(APIView):
    permission_classes = (IsAuthenticated, IsOwner,)

    def get_amount_for_category(self, expense_list, category):
        expenses = expense_list.filter(category=category)
        amount = 0
        
        for expense in expenses:
            amount += expense.amount
        return {'amount': str(amount)}

    def get_category(self, expenses):
        return expenses.category

    def get(self, request):
        today_date = datetime.date.today()
        ayear_ago = today_date - datetime.timedelta(days=30 * 12)
        expenses = Expenses.objects.filter(user=request.user, date__gte=ayear_ago, date__lte=today_date)

        final = {}
        categories = list(set(map(self.get_category, expenses)))

        print('Expenses: ', expenses)
        print('Categories: ', categories)
        
        for expense in expenses:
            for category in categories:
                final[category] = self.get_amount_for_category(expenses, category)
                
        return Response({'expense_category_data': final}, status=status.HTTP_200_OK)

class IncomeSummaryStats(APIView):
    # permission_classes = (IsAuthenticated, IsOwner,)
    
    def get_category(self, income):
        return income.source
    
    def get_amount_for_source(self, income_list, source):
        incomes = income_list.filter(source=source)
        amount = 0
        
        for income in incomes:
            amount += income.amount
        
        return {'amount': str(amount)}

    def get(self, request):
        today_date = datetime.date.today()
        ayear_ago = today_date - datetime.timedelta(days=30 * 12)
        incomes = Income.objects.filter(user=request.user, date__gte=ayear_ago, date__lte=today_date)
        
        final = {}
        sources = list(map(self.get_category, incomes))

        for income in incomes:
            for source in sources:
                final[source] = self.get_amount_for_source(incomes, source)
        # import pdb
        # pdb.set_trace()
        return Response({'income_category_data': final}, status=status.HTTP_200_OK)