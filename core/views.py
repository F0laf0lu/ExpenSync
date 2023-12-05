from django.shortcuts import redirect, render
from core.models import Expense, Category
from django.db.models import Sum, Count
from django.utils import timezone
import calendar
from datetime import timedelta   


current_date = timezone.now()

def get_month_range(input_date):
    # Get the first day of the month
    first_day = input_date.replace(day=1)

    # Calculate the last day of the month
    _, last_day = calendar.monthrange(input_date.year, input_date.month)
    last_day = input_date.replace(day=last_day)

    return first_day, last_day

def get_week_range(input_date):
    # Calculate the start of the week (Monday)
    start_of_week = input_date - timedelta(days=input_date.weekday())

    # Calculate the end of the week (Sunday)
    end_of_week = start_of_week + timedelta(days=6)

    return start_of_week, end_of_week


# Views

def home(request):
    user_id = request.user.id
    expenses = Expense.objects.filter(
        user=user_id).order_by("-created_on")[0:5]
    category = Category.objects.filter(user=user_id) 

    # Get number of expenses in a category
    cat_count = Category.objects.annotate(expense_len = Count("expenses"))
    cat_count = cat_count.order_by("-expense_len")[:5]

    # Get number of expenses in a category
    cat_sum = Category.objects.annotate(expense_sum = Sum("expenses__amount"))
    cat_sum = cat_sum.order_by("-expense_sum")[:5]

    total = Expense.objects.filter(
            user=user_id).aggregate(Sum('amount'))['amount__sum']

    
    context = {
        'expenses' : expenses,
        'category':category,
        'total':total,
        'cat_count':cat_count, 
        "cat_sum": cat_sum
    }

    return render (request, 'index.html', context)

def expenses(request):
    user_id = request.user
    expenses = Expense.objects.filter(
        user=user_id).order_by("-created_on")
    
    category = Category.objects.filter(user=user_id)

    total = Expense.objects.filter(
            user=user_id).aggregate(Sum('amount'))['amount__sum']

    context = {
        'expenses' : expenses,
        'total':total,
        'category':category
    }

    return render(request, 'expenses.html', context)

def transationfilters(request):
    user_id = request.user
    total = Expense.objects.filter(
            user=user_id).aggregate(Sum('amount'))['amount__sum']
    expenses = ""
    # Search Query
    query = request.GET.get('q')

    if query:
        expenses = Expense.objects.filter(description__icontains=query)
        

    # Time Filter
    timequery = request.GET.get('timefilter')
    if timequery == 'thisweek':
        start_week, end_week = get_week_range(current_date)
        expenses = Expense.objects.filter(created_on__range=(start_week, end_week))
    if timequery == 'thismonth':
        start_month, end_month = get_month_range(current_date)
        expenses = Expense.objects.filter(created_on__range=(start_month, end_month))
    if timequery == 'thisyear':
        expenses = Expense.objects.filter(created_on__year=2023) #fix year

    context = {
    'query':query,
    'timequery':timequery,
    'expenses' : expenses,
    'total':total,
    'expenses':expenses,
    }
    
    return render(request, "expenses.html", context)

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
    if request.method == 'POST':
        expense.delete()
        if Expense.objects.filter(category=category).count() == 0:
            category.delete()
        return redirect("home")
    
    context = {
        'expense':expense
    }
    return render(request, "delete_expense.html", context)

def updateexpense():
    pass