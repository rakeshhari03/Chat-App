from django.shortcuts import render,redirect
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.utils import timezone
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return redirect('user_list')
    return render(request, 'index.html')   

def register(request):
    if request.user.is_authenticated:
        return redirect('user_list')  
    
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, "register.html", {"form": form})

def login(request):
    if request.user.is_authenticated:
        return redirect('user_list')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_url = request.POST.get("next")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            if next_url:
                return redirect(next_url)

            return redirect("user_list")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

def logout(request):
    # Update user offline status and last_seen before logging out
    if request.user.is_authenticated:
        request.user.is_online = False
        request.user.last_seen = timezone.now()
        request.user.save(update_fields=['is_online', 'last_seen'])
    
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')
