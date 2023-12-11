from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.userlogin, name="login"),
    path('logout/', views.userlogout, name='logout'),
    path('signup/', views.usersignup, name='signup'),
]
