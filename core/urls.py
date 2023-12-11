from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('add-expense/', views.addexpense, name='add-expense'),
    path('delete-expense/<int:id>/', views.deleteexpense, name='delete-expense'),
    path('update-expense/<int:id>/', views.updateexpense, name='update-expense'),
    path('transaction/', views.transactions, name='transaction'),
    path('transactions/search/', views.transationfilters, name='search-filter'),
    path('reports/', views.reports, name='reports')
]
