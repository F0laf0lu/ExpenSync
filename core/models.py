from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.urls import reverse
# Create your models here.

class Category(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f'{self.name}'


class Transaction(models.Model):
    INCOME = 'income'
    EXPENSE = 'expense'

    TRANSACTION_CHOICES = [
        (INCOME, ('Income')),
        (EXPENSE,('Expense')),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="transactions")
    
    transaction_type = models.CharField(max_length=100, choices = TRANSACTION_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='transactions')

    description = models.CharField(max_length=200, null=True, blank=True)
    amount = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f'{self.transaction_type} - {self.amount}' 

