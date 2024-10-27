from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/',views.signup, name='signup'),
    path('signin/',views.signin, name='signin'),
    path('dashboard/',views.dasboard, name='dashboard'),
    path('admin',views.admin_signin, name="admin_signin")
]
