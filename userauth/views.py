from django.shortcuts import render
from django.contrib.auth import get_user_model
from . forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.

def userlogin(request):
    User = get_user_model()
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except: 
            messages.error(request, 'user does not exist')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'email and password do not match')
    context = {}
    return render(request, 'userauth/login.html', context)


def userlogout(request):
    logout(request)
    return redirect('login')

def usersignup(request):
    signupform = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()
            return redirect('login')
        else:
            messages.error(request, 'Error during registration')


    context = {
        'signupform':signupform
    }
    return render(request, "userauth/signup.html", context)

