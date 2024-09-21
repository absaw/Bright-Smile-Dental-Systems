from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
from .forms import CustomUserCreationForm
from .decorators import redirect_authenticated_user

@ensure_csrf_cookie
@redirect_authenticated_user
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, ("Invalid username or password."))
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You were logged out!"))
    return redirect('login')  # Changed this line to redirect to login page

@ensure_csrf_cookie
def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration successful!"))
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'authenticate/register_user.html', {
        'form': form,
    })
    
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

@ensure_csrf_cookie
def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'authenticate/register_user.html', {'form': form})