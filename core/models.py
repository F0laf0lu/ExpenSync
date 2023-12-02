from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

class Category(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f'{self.name}'

class Expense(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    description = models.CharField(max_length=200)
    amount = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.category} - {self.name}'
