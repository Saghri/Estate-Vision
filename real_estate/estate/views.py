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


# # --------------------------------------- Register View

# from django.contrib.auth import login
# from django.contrib.auth import get_user_model
# from django.shortcuts import render, redirect
# from .forms import RegisterForm

# User = get_user_model()

# def register_view(request):
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get("username")
#             email = form.cleaned_data.get("email")
#             password1 = form.cleaned_data.get("password1")
#             password2 = form.cleaned_data.get("password2")
            
#             # Check if passwords match
#             if password1 != password2:
#                 form.add_error('password2', 'Passwords do not match')
#             else:
#                 # Create the user
#                 user = User.objects.create_user(username=username, email=email, password=password1)
                
#                 # Authenticate with the specified backend
#                 user.backend = 'django.contrib.auth.backends.ModelBackend'
                
#                 # Login the user
#                 login(request, user)
                
#                 return redirect('login')  # Redirect to the login page after signup
#     else:
#         form = RegisterForm()
    
#     return render(request, 'accounts/Signup.html', {'form': form})


# # -------------------------Login View

# from django.shortcuts import redirect

# from django.contrib.auth import authenticate, login
# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User

# def login_view(request):
#     error_message = None 
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         # Find the user by email and pass the username to authenticate()
#         try:
#             user = User.objects.get(email=email)
#             user = authenticate(request, username=user.username, password=password)
#         except User.DoesNotExist:
#             user = None

#         if user is not None:
#             login(request, user)
#             return redirect('user_dashboard')
#         else:
#             error_message = "Invalid credentials"
#     return render(request, 'accounts/login.html', {'error': error_message})

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from .forms import RegisterForm
from .models import Profile

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is verified
            user.save()

            token = get_random_string(length=32)
            Profile.objects.filter(user=user).update(email_verification_token=token)

            verification_link = f"{request.scheme}://{request.get_host()}/verify-email/{token}/"
            send_mail(
                'Verify your email',
                f'Please click the link to verify your email: {verification_link}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            
            return render(request, 'accounts/verification_sent.html')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/Signup.html', {'form': form})

from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .models import Profile

User = get_user_model()

def verify_email(request, token):
    try:
        profile = Profile.objects.get(email_verification_token=token)
        user = profile.user
        user.is_active = True
        user.save()
        profile.email_verified = True
        profile.email_verification_token = ''
        profile.save()
        
        # Specify the authentication backend
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        
        return redirect('user_dashboard')
    except Profile.DoesNotExist:
        return render(request, 'accounts/verification_failed.html')

# def login_view(request):
#     error_message = None 
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         try:
#             user = User.objects.get(email=email)
#             user = authenticate(request, username=user.username, password=password)
#             if user is not None:
#                 if user.profile.email_verified:
#                     login(request, user)
#                     return redirect('user_dashboard')
#                 else:
#                     error_message = "Please verify your email before logging in."
#             else:
#                 error_message = "Invalid credentials"
#         except User.DoesNotExist:
#             error_message = "Invalid credentials"
    
#     return render(request, 'accounts/login.html', {'error': error_message})

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    error_message = None 
    if request.method == "POST":
        username_or_email = request.POST.get("username")  # Assume the form field is named "username"
        password = request.POST.get("password")

        # Try to authenticate with username
        user = authenticate(request, username=username_or_email, password=password)
        
        if user is None:
            # If username authentication fails, try with email
            user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            if user.is_active:
                if user.profile.email_verified:
                    login(request, user)
                    return redirect('user_dashboard')
                else:
                    error_message = "Please verify your email before logging in."
            else:
                error_message = "Your account is not active. Please check your email for verification."
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

def analysis_page_view(request):
    return render(request, 'myapp/analysis.html')

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


from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Set non-GUI backend for matplotlib

def dashboard(request):
    return render(request, 'myapp/user_dashboard.html')

@csrf_exempt
def analyze_data(request):
    if request.method == 'POST':
        file = request.FILES['file']
        algorithm = request.POST.get('algorithm')
        
        # Read CSV file
        df = pd.read_csv(file)
        
        # Display top 5 records for user review
        top_records = df.head(5).to_json(orient='records')
        
        # Prepare data
        le_property = LabelEncoder()
        le_location = LabelEncoder()
        df['Property Type'] = le_property.fit_transform(df['Property Type'])
        df['Location'] = le_location.fit_transform(df['Location'])
        
        # Features and target variable
        X = df[['Property Type', 'Age', 'Location']]
        y = df['Sale Price']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Select and apply algorithm
        if algorithm == 'linear_regression':
            model = LinearRegression()
        elif algorithm == 'decision_tree':
            model = DecisionTreeRegressor()
        elif algorithm == 'random_forest':
            model = RandomForestRegressor()
        else:
            return JsonResponse({'error': 'Invalid algorithm'})
        
        model.fit(X_train, y_train)
        accuracy = model.score(X_test, y_test)
        
        # Generate predictions for visualization
        predictions = model.predict(X_test[:10])
        actual = y_test[:10].tolist()
        
        # Generate analysis plots
        analysis_images = generate_analysis_charts(df, le_property, le_location)
        
        result = {
            'algorithm': algorithm,
            'accuracy': accuracy,
            'predictions': predictions.tolist(),
            'actual': actual,
            'top_records': json.loads(top_records),
            'analysis_images': analysis_images  # Contains base64-encoded charts
        }
        
        return JsonResponse(result)
    
    return JsonResponse({'error': 'Invalid request method'})

def generate_analysis_charts(df, le_property, le_location):
    # Function to generate charts and return their base64 representations
    charts = []
    
    # Chart 1: Distribution of Property Types
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=df, x='Property Type', ax=ax)
    # Set x-axis labels to original property types
    ax.set_xticklabels(le_property.inverse_transform(range(len(le_property.classes_))))
    # ax.set_title("Distribution of Property Types")
    ax.set_xlabel("Property Type")
    ax.set_ylabel("Count")
    charts.append(encode_image(fig))

    # Chart 2: Distribution of Sale Price by Location
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x='Location', y='Sale Price', ax=ax)
    # Set x-axis labels to original location names
    ax.set_xticklabels(le_location.inverse_transform(range(len(le_location.classes_))))
    # ax.set_title("Distribution of Sale Price by Location")
    ax.set_xlabel("Location")
    ax.set_ylabel("Sale Price")
    charts.append(encode_image(fig))

    # Chart 3: Sales over time
    df['Sale Date'] = pd.to_datetime(df['Sale Date'])
    monthly_sales = df.resample('ME', on='Sale Date').size()
    fig, ax = plt.subplots(figsize=(10, 6))
    monthly_sales.plot(ax=ax)
    # ax.set_title("Sales Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Sales")
    charts.append(encode_image(fig))

    # Chart 4: Sale Price Distribution by Age Group
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x='Age', y='Sale Price', ax=ax)
    # ax.set_title("Sale Price Distribution by Age Group")
    ax.set_xlabel("Age")
    ax.set_ylabel("Sale Price")
    charts.append(encode_image(fig))
    
    return charts

def encode_image(fig):
    # Save plot as a PNG image and encode in base64
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{image_base64}"


# -------------------------------------------------------
