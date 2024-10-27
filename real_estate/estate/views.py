from django.shortcuts import render

def index(request):
    return render(request, 'myapp/mainpage.html')

def signup(request):
    return render(request, 'myapp/signup.html')

def signin(request):
    return render(request, 'myapp/Sign-in.html')

def dasboard(request):
    return render(request, 'myapp/Dashboard.html')

def admin_signin(request):
    return render(request, 'myapp/Admin.html')