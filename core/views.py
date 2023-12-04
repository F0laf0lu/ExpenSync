from django.shortcuts import redirect, render
from core.models import Expense, Category
from django.db.models import Sum

# Create your views here.

def home(request):
    user_id = request.user.id
    expenses = Expense.objects.filter(
        user=user_id).order_by("-created_on")[0:5]
    category = Category.objects.filter(user=user_id) 

    total = Expense.objects.filter(
            user=user_id).aggregate(Sum('amount'))['amount__sum']
    
    category_count = Category.objects.get(user=user_id).expenses.all().count 
    
    context = {
        'expenses' : expenses,
        'category':category,
        'total':total
    }

    return render (request, 'index.html', context)

def expenses(request):
    user_id = request.user
    total = 0
    expenses = Expense.objects.filter(
        user=user_id).order_by("-created_on")
    for i in expenses:
        total += i.amount

    context = {
        'expenses' : expenses,
        'total':total
    }

    return render(request, 'expenses.html', context)

def addexpense(request):
    user = request.user
    category_list = Category.objects.filter(user=user)
    
    if request.method == 'POST':
        category, created = Category.objects.get_or_create(
            name=request.POST.get('category'),
            user=user)

        Expense.objects.create(
            user = request.user,
            amount = request.POST.get('amount'),
            description = request.POST.get('description'),
            category = category
        )
        return redirect("home")
    context = {
        'category_list':category_list
    }

    return render (request, 'add_expense.html', context)

def deleteexpense(request, id):
    expense = Expense.objects.get(id=id)
    category = expense.category
    print(Expense.objects.filter(category=category).count())
    if request.method == 'POST':
        expense.delete()
        if Expense.objects.filter(category=category).count() == 0:
            category.delete()
        return redirect("home")
    
    context = {
        'expense':expense
    }
    return render(request, "delete_expense.html", context)