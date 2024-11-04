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


# # views.py
# import pandas as pd
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json

# @csrf_exempt
# def upload_csv(request):
#     if request.method == 'POST' and request.FILES.get('csv_file'):
#         csv_file = request.FILES['csv_file']
#         df = pd.read_csv(csv_file)
#         # 
#         # Process the data and generate default graphs
#         columns = df.columns.tolist()
#         default_graphs = generate_default_graphs(df)
#         quick_analysis = generate_quick_analysis(df)
        
#         # Save the DataFrame to the session or database for further analysis
#         request.session['df'] = df.to_json()
        
#         return JsonResponse({
#             'success': True,
#             'columns': columns,
#             'default_graphs': default_graphs,
#             'quick_analysis': quick_analysis
#         })
#     return JsonResponse({'success': False})

# @csrf_exempt
# def analyze(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         algorithm = data.get('algorithm')
#         graphs = data.get('graphs')
        
#         # Retrieve the DataFrame from the session or database
#         df = pd.read_json(request.session.get('df'))
        
#         # Perform analysis based on the selected algorithm and graph types
#         analysis_results = perform_analysis(df, algorithm, graphs)
        
#         return JsonResponse({
#             'success': True,
#             'graphs': analysis_results
#         })
#     return JsonResponse({'success': False})

# @csrf_exempt
# def generate_report(request):
#     if request.method == 'GET':
#         # Retrieve the DataFrame and analysis results
#         df = pd.read_json(request.session.get('df'))
        
#         # Generate a comprehensive report
#         report = generate_comprehensive_report(df)
        
#         return JsonResponse({
#             'success': True,
#             'report': report
#         })
#     return JsonResponse({'success': False})

# # Helper functions for data analysis and visualization
# def generate_default_graphs(df):
#     # Implement logic to generate default graphs based on the dataset
#     pass

# def generate_quick_analysis(df):
#     # Implement logic to generate quick analysis results
#     pass

# def perform_analysis(df, algorithm, graphs):
#     # Implement logic to perform analysis based on the selected algorithm and graph types
#     pass

# def generate_comprehensive_report(df):
#     # Implement logic to generate a comprehensive report based on the analysis
#     pass

# ----------------------------------------------------

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
