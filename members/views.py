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
            #login saves the user's id and password in the session
            return redirect('home')
        else:
            messages.error(request, ("Invalid username or password."))
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

@ensure_csrf_cookie
@redirect_authenticated_user
def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Authenticate the user first
            authenticated_user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, "Registration successful!")
                return redirect('home')
           
    else:
        form = CustomUserCreationForm()
    return render(request, 'authenticate/register_user.html', {'form': form})