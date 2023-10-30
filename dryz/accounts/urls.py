from django.urls import path
from . import views
urlpatterns = [
    path('', views.UserSignin, name='user_signin'),
    path('register/', views.UserSignup, name='user_signup'),
    path('signin_otp/', views.otp_signin, name='signin_otp'),
    path('signup_otp/', views.otp_signup, name='signup_otp'),
    path('logout/', views.UserLogout, name='user_logout'),
    path('login_email_otp/', views.signin_email_otp, name='login_email_otp'),
    path('forgot_password/', views.ForgotPassword, name='forgot_password'),
    path('otp_forgot_password/', views.ForgotPasswordOtp,
         name='otp_forgot_password'),
    path('confirm_password', views.ConfirmPassword, name='confirm_password'),
    path('resend_otp', views.ResentOtp, name='resend_otp'),
    path('wallet', views.wallet, name='wallet'),
]
