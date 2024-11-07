# from django.urls import path
# from . import views

# from django.contrib.auth import views as auth_views

# urlpatterns = [
#     path('', views.index, name='index'),
#     path('signup/',views.signup, name='signup'),
#     path('login/',views.login, name='login'),
#     path('dashboard/',views.dashboard, name='dashboard'),
#     path('admin',views.admin_login, name="admin_signin"),


#     # path('signup/', views.signup, name='signup'),
#     # path('activate/<uidb64>/<token>/', views.activate, name='activate'),
#     # path('signin/', views.signin, name='signin'),  # Signin view can be added later
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page_view, name='home'),
    path('accounts/signup/', views.register_view, name='Signup'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('user_dashboard/', views.dashboard, name='user_dashboard'),
    path('user_dashboard/', views.ProtectedView.as_view(), name='dashboard'),
    path('analysis_page/', views.analysis_page_view, name='analysis_page'),

    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),

    path('analyze/', views.analyze_data, name='analyze_data'),
]
