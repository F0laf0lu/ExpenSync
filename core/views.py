from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from core.models import Transaction, Category
from . forms import TransactionForm
from django.db.models import Sum
from django.contrib import messages


# Views
def home(request):
    
    print()

    form = TransactionForm()
    user_id = request.user.id

    transactions = Transaction.objects.filter(
        user=user_id).order_by("-created_on")[0:5]
    
    category = Category.objects.filter(user=user_id) 

    income_total = Transaction.objects.filter(user=user_id).filter(transaction_type="income").aggregate(Sum('amount'))['amount__sum']
    
    if income_total is None:
        income_total = 0

    expense_total = Transaction.objects.filter(
            user=user_id).filter(transaction_type="expense").aggregate(Sum('amount'))['amount__sum']
    
    if expense_total is None:
        expense_total = 0
        balance = income_total - expense_total
    else:
        balance = income_total - expense_total
        
    data = []
    expense_category = Category.objects.filter(
        transactions__transaction_type='expense').filter(user=user_id).annotate(sum = Sum('transactions__amount'))
    cat = expense_category.values('name','sum')
    for i in cat:
        data.append((i['name'], i['sum']))



    context = {
        'transactions' : transactions,
        'category':category,
        'expense_total':expense_total,
        'income_total':income_total,
        'balance':balance,
        'form':form, 
        'data':data
    }
    return render (request, 'index.html', context)

def transactions(request): 
    form = TransactionForm()
    user_id = request.user
    transactions = Transaction.objects.filter(
        user=user_id).order_by("-updated_on","-created_on")
    
    category = Category.objects.filter(user=user_id)

    total = Transaction.objects.filter(
            user=user_id).aggregate(Sum('amount'))['amount__sum']

    context = {
        'transactions' : transactions,
        'total':total,
        'category':category,
        'form':form
    }

    return render(request, 'transactions.html', context)

def addexpense(request):
    user = request.user
    if request.method == 'POST':
            category_name = request.POST.get('category')
            category, created = Category.objects.get_or_create(name=category_name)

            trans_type = request.POST.get('transaction_type')
            amount = request.POST.get('amount')
            description = request.POST.get('description')

            Transaction.objects.create(
                user=user,
                category=category,
                transaction_type=trans_type,
                amount=amount,
                description=description
            )
            messages.success(request, 'Transaction creation successful!', extra_tags=
            'alert')
            return redirect("home")
    else:
        messages.warning(request, 'Error occured')
    
    return redirect("home")

def updateexpense(request, id):
    view_name = "update"
    user = request.user
    form = TransactionForm()
    transaction = get_object_or_404(Transaction, id=id)
    category_data = transaction.category

    updateform = TransactionForm(instance=transaction)
    category_list = Category.objects.filter(user=user)
    transactions = Transaction.objects.filter(user=user).order_by("-updated_on","-created_on")

    if request.method == 'POST':
        category, created = Category.objects.get_or_create(
            name=request.POST.get('category'),
            user=user)

        if request.POST.get('submit_button') == 'update-expense':
            updateform = TransactionForm(request.POST, instance=transaction)
            Transaction.objects.filter(id=id).update(
                description=request.POST.get('description'),
                amount=request.POST.get('amount'),
                transaction_type=request.POST.get('transaction_type'),
                category=category,
            ) 
            return redirect("transaction") 
        elif request.POST.get('submit_button') == 'delete-expense':
            return redirect("delete-expense", transaction.id )

    context = {
        'category_list':category_list, 
        'category_data':category_data,
        'transaction':transaction,
        'transactions':transactions,
        'updateform':updateform,
        'view_name':view_name,
        'form':form
    }
    return render (request, 'transactions.html', context)


def deleteexpense(request, id):
    expense = Transaction.objects.get(id=id)
    category = expense.category
    if request.method == 'POST':
        expense.delete()
        if Transaction.objects.filter(category=category).count() == 0:
            category.delete()
        return redirect("transaction")
    
    context = {
        'expense':expense
    }
    return render(request, "delete_expense.html", context)


def reports(request):
    user = request.user

    # Pie Chart Data
    data = []
    expense_category = Category.objects.filter(
        transactions__transaction_type='expense').filter(user=user).annotate(sum = Sum('transactions__amount'))
    cat = expense_category.values('name','sum')
    for i in cat:
        data.append((i['name'], i['sum']))


    # Column Chart Data
    columnchartdata = []
    months  = Transaction.objects.filter(user=user).values('updated_on__month').distinct()

    for i in months:
        exp_sum = Transaction.objects.filter(user=user).filter(
            updated_on__month=i['updated_on__month']
            ).filter(
            transaction_type='expense'
            ).aggregate(
                sum = Sum('amount'))
        
        inc_sum = Transaction.objects.filter(user=user).filter(
            updated_on__month=i['updated_on__month']
            ).filter(
            transaction_type='income'
            ).aggregate(
                sum = Sum('amount'))
        
        balance = exp_sum['sum'] - inc_sum['sum']
        
        # print([i['updated_on__month'],exp_sum['sum'], inc_sum['sum'], balance])

        columnchartdata.append([i['updated_on__month'], exp_sum['sum'], inc_sum['sum'], balance])


    month_dict = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec',}

    sortedcolumnchartdata = sorted(columnchartdata)

    for i in sortedcolumnchartdata:
        i[0] = month_dict[i[0]]

    context = {
        'data':data,
        'sortedcolumnchartdata':sortedcolumnchartdata
    }


    return render(request, 'reports.html', context)

