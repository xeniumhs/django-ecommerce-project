from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import UserLoginForm
from accounts.models import Profile


from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            user = form.save(commit=False)  # Do not save the user yet

            # Save the user first so that it has a primary key for filtering
            user.save()

            # Now, check if the profile exists for the user
            profile = Profile.objects.filter(user=user).first()
            if not profile:
                # Create and save the profile if it does not exist
                profile = Profile(user=user)
                profile.user_type = 'customer'  # Set default user type
                profile.save()

            messages.success(request, "Registration successful. You can now log in.")
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                
                # Check if user is a superuser
                if user.is_superuser:
                    return redirect('product:home')  # Redirect superusers to Django admin dashboard
                
                # Check user profile type
                if user.profile.user_type == 'admin':
                    return redirect('product:home')  # Replace with actual admin dashboard redirect
                elif user.profile.user_type == 'customer':
                    return redirect('product:home')  # Corrected to use the 'product' namespace
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})



from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    logout(request)
    return redirect('accounts:login')
