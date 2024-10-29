# To handle views and redirects
from django.shortcuts import render, redirect
# To Import auth functions form Django
from django.contrib.auth import authenticate, login, logout
# The login_required decorator to protect views
from django.contrib.auth.decorators import login_required
# For class-based views[CBV]
from django.contrib.auth.mixins import LoginRequiredMixin
# For class-based views[CBV]
from django.views import View
#  Import the User class (model)
from django.contrib.auth.models import User
# Import the RegisterForm from forms.py
from .forms import RegisterForm


# def register_view(request):
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get("username")
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = User.objects.create_user(username=username,email=email, password=password)
#             login(request, user)
#             return redirect('login')
#     else:
#         form = RegisterForm()
#     return render(request, 'accounts/Signup.html', {'form':form})

from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            
            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # Authenticate with the specified backend
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            
            # Login the user
            login(request, user)
            
            return redirect('login')  # Redirect to the dashboard after signup
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/Signup.html', {'form': form})


# def login_view(request):
#     error_message = None 
#     if request.method == "POST":  
#         # username = request.POST.get("username")  
#         email= request.POST.get("email")
#         password = request.POST.get("password")  
#         # user = authenticate(request, username=username, password=password)  
#         user = authenticate(request, email=email, password=password)  
#         if user is not None:  
#             login(request, user)  
#             next_url = request.POST.get('next') or request.GET.get('next') or 'home'  
#             return redirect(next_url) 
#         else:
#             error_message = "Invalid credentials"  
#     return render(request, 'accounts/login.html', {'error': error_message})

from django.shortcuts import redirect

def login_view(request):
    error_message = None 
    if request.method == "POST":  
        email = request.POST.get("email")  
        password = request.POST.get("password")  
        user = authenticate(request, email=email, password=password)  # Use email instead of username
        if user is not None:  
            login(request, user)  
            # Redirect to the dashboard page after login
            return redirect('user_dashboard')  
        else:
            error_message = "Invalid credentials"  
    return render(request, 'accounts/login.html', {'error': error_message})




def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    else:
        return redirect('home')

def main_page_view(request):
    return render(request, 'myapp/mainpage.html')

# Home View
# Using the decorator 
@login_required
# def home_view(request):
#     return render(request, 'myapp/mainpage.html')

def dashboard(request):
    return render(request, 'myapp/user_dashboard.html')

# Protected View 
class ProtectedView(LoginRequiredMixin, View):
    login_url = '/login/'
    # 'next' - to redirect URL
    redirect_field_name = 'redirect_to'
    
    def get(self, request):
        return render(request, 'myapp/user_dashboard.html')

# -------------------------------------------------------


# def index(request):
#     return render(request, 'myapp/mainpage.html')

# def signup(request):
#     return render(request, 'myapp/signup.html')

# def login(request):
#     return render(request, 'myapp/Login.html')

# def dashboard(request):
#     return render(request, 'myapp/Dashboard.html')

# def admin_login(request):
#     return render(request, 'myapp/admin_login.html')

