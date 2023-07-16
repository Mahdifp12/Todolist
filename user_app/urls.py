from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="register-user-page"),
    path('login/', views.LoginView.as_view(), name="login-user-page"),
    path('forgot-password/', views.ForgetPasswordView.as_view(), name="forgot-password-page"),
    path('reset-password/', views.ResetPasswordView.as_view(), name="reset-password-page"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
]
