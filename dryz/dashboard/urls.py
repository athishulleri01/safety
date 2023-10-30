from django.urls import path
from . import views

urlpatterns = [
    path('admin_dash/', views.DashBoard, name="dashboard"),
    path('users_details/', views.UsersDetails, name="users_details"),
    path('block_user/<int:user_id>/', views.UserBlock, name="block_user"),
    path('admin_login', views.AdminLogin, name="admin_login"),
    path('admin_logout', views.AdminLogout, name="admin_logout"),
    path('get-sales-revenue/', views.get_sales_revenue,
         name='get_sales_revenue'),
]
