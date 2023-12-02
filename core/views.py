from django.shortcuts import render
from core.models import Expense, Category

# Create your views here.

def home(request):
    user_id = request.user
    expenses = Expense.objects.filter(user=user_id)
    category = Category.objects.filter(user=user_id)
    total = 0

    for i in expenses:
        total += i.amount

    context = {
        'expenses' : expenses,
        'category':category,
        'total':total
    }

    return render (request, 'index.html', context)