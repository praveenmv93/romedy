from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from e_app.models import UserProfile

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        passw = request.POST.get('password')
        user = authenticate(request, username=username, password=passw)
        if user is not None:
            login(request, user)
            # Check user role and redirect
            try:
                profile = user.profile
                if profile.role == 'doctor':
                    return redirect('doctor_dashboard')
                elif profile.role == 'staff':
                    return redirect('staff_dashboard')
                else:
                    return redirect('home page')
            except UserProfile.DoesNotExist:
                # Default fallback
                return redirect('home page')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        passw = request.POST.get('password')
        phone = request.POST.get('phone')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'signup.html')
            
        user = User.objects.create_user(username=username, email=email, password=passw)
        UserProfile.objects.create(user=user, role='patient', phone=phone)
        
        # Log the user in
        login(request, user)
        messages.success(request, "Registration successful!")
        return redirect('home page')
        
    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect('home page')
