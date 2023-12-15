import os
from django.shortcuts import render
from django.contrib.auth import get_user_model
from . forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

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


@login_required
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

@login_required
def usersprofile(request, pk):
    user = get_object_or_404(get_user_model(), id=pk)
    form = CustomUserChangeForm(instance=user)

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)

    context = {'form':form}
    return render(request,"userauth/profile.html", context)


@login_required
def deleteprofileimage(request, pk):
    user = get_object_or_404(get_user_model(), id=pk)
    avatar_path = user.avatar.path
    if os.path.exists(avatar_path):
            os.remove(avatar_path)

    user.avatar = 'avatar.svg'
    user.save()
    return redirect("profile", pk=user.id)