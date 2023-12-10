from django.shortcuts import get_object_or_404, redirect, render
from core.models import Transaction, Category
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime
import calendar
from django.core.paginator import Paginator
from datetime import timedelta   



current_date = timezone.now()
print(current_date)

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
    expenses = Transaction.objects.filter(
        user=user_id).order_by("-created_on")[0:5]
    category = Category.objects.filter(user=user_id) 

    # Get number of expenses in a category
    cat_count = Category.objects.annotate(expense_len = Count("transactions"))
    cat_count = cat_count.order_by("-expense_len")[:5]

    # Get number of expenses in a category
    cat_sum = Category.objects.annotate(expense_sum = Sum("transactions__amount"))
    cat_sum = cat_sum.order_by("-expense_sum")[:5]

    total = Transaction.objects.filter(
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
    expenses = Transaction.objects.filter(
        user=user_id).order_by("-created_on")
    
    category = Category.objects.filter(user=user_id)


    # paginator = Paginator(expenses, 5)
    # page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number)


    total = Transaction.objects.filter(
            user=user_id).aggregate(Sum('amount'))['amount__sum']

    context = {
        'expenses' : expenses,
        'total':total,
        'category':category,
        # 'page_obj':page_obj
    }

    return render(request, 'expenses.html', context)

def transationfilters(request):
    user_id = request.user
    category = Category.objects.filter(user=user_id)
    total = Transaction.objects.filter(
            user=user_id).aggregate(Sum('amount'))['amount__sum']
    expenses = ""
    # Search Query
    query = request.GET.get('q')

    if query:
        expenses =Transaction.objects.filter(description__icontains=query)
        

    # Time Filter
    timequery = request.GET.get('timefilter')
    if timequery == 'thisweek':
        start_week, end_week = get_week_range(current_date)
        expenses = Transaction.objects.filter(created_on__range=(start_week, end_week)).order_by("-created_on")
    if timequery == 'thismonth':
        start_month, end_month = get_month_range(current_date)
        expenses = Transaction.objects.filter(created_on__range=(start_month, end_month))
    if timequery == 'thisyear':
        expenses = Transaction.objects.filter(created_on__year=2023) #fix year

    # date range
    date_from_obj = datetime.strptime(request.GET.get('date_from'), "%Y-%m-%d")
    date_from = timezone.make_aware(date_from_obj)

    date_to_obj = datetime.strptime(request.GET.get('date_to'), "%Y-%m-%d")
    date_to = timezone.make_aware(date_to_obj)
    if date_from:
        if date_to:
            expenses = Transaction.objects.filter(created_on__date__range=(date_from, date_to))

    # Category Query
    cat_query = request.GET.get("category_query")
    cat = Category.objects.get(name=cat_query)

    if cat_query:
        expenses = cat.expenses.all()

    context = {
    'query':query,
    'timequery':timequery,
    'expenses' : expenses,
    'total':total,
    'expenses':expenses,
    'category':category
    }
    
    return render(request, "expenses.html", context)


def addexpense(request):
    user = request.user
    category_list = Category.objects.filter(user=user)
    
    if request.method == 'POST':
        category, created = Category.objects.get_or_create(
            name=request.POST.get('category'),
            user=user)

        Transaction.objects.create(
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
    expense = Transaction.objects.get(id=id)
    category = expense.category
    if request.method == 'POST':
        expense.delete()
        if Transaction.objects.filter(category=category).count() == 0:
            category.delete()
        return redirect("home")
    
    context = {
        'expense':expense
    }
    return render(request, "delete_expense.html", context)


def updateexpense(request, id):
    user = request.user
    expense = get_object_or_404(Transaction, id=id)
    category_list = Category.objects.filter(user=user)
    
    if request.method == 'POST':
        category, created = Category.objects.get_or_create(
            name=request.POST.get('category'),
            user=user)

        expense.amount = request.POST.get('amount')
        expense.category = category
        expense.description = request.POST.get('description')
        expense.save()
        return redirect("home")
    context = {
        'category_list':category_list, 
        'expense':expense 
    }
    return render (request, 'update_expense.html', context)


def reports(request):
    return render(request, 'reports.html')