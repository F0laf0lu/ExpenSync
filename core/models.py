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

class Expense(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='category')
    description = models.CharField(max_length=200)
    amount = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)

    @property
    def totalexpense(self):
        # Calculate the total expenses for the user
        total_expenses = Expense.objects.filter(
            user=self.user).aggregate(Sum('amount'))['amount__sum']
        return total_expenses


    def __str__(self) -> str:
        return f'{self.category} - {self.description}'
    
    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})

