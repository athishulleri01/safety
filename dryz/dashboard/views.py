from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import CustomUser
from order.models import Order, OrderItem
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.utils import timezone
from django.db.models import Q
# Create your views here.

def AdminLogin(request):
    if 'admin_email' in request.session:
        return redirect('dashboard')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if email and password are provided and not empty
        if email is not None and password is not None and email.strip() == '' and password.strip() == '':
            # Display an error message and redirect back to the sign-in page if fields are blank
            messages.error(request, "Fields can't be blank")
            return redirect('admin_login')

        # Authenticate the user with provided email and password
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                request.session['admin_email'] = email
                return redirect('dashboard')
    return render(request, 'adminside/admin_login.html')


def AdminLogout(request):
    if 'admin_email' in request.session:
        logout(request)

    return redirect('dashboard')


def DashBoard(request):
    if 'admin_email' in request.session:
        email = request.session['admin_email']
        user = CustomUser.objects.get(email=email)

        orders=Order.objects.filter(status='Delivered')
        order_count = orders.count()
        total_amount=0
        customers=CustomUser.objects.filter(is_superuser=False).count()
        for item in orders:
            total_amount=total_amount+item.total_price

        no_deliverd = OrderItem.objects.filter(status='Delivered').count()
        no_cancel =  OrderItem.objects.filter(status='Cancelled').count()
        no_return =  OrderItem.objects.filter(status='Returned').count()

        current_year = timezone.now().year

        # Calculate monthly sales for the current year
        monthly_sales = Order.objects.filter(
            created_at__year=current_year
        ).annotate(month=ExtractMonth('created_at')).values('month').annotate(total_sales=Sum('total_price')).order_by(
            'month')

        # Create a dictionary to hold the monthly sales data
        monthly_sales_data = {month: 0 for month in range(1, 13)}

        for entry in monthly_sales:
            month = entry['month']
            total_sales = entry['total_sales']
            monthly_sales_data[month] = total_sales

        context = {
            'user': user,
            'total_amount': total_amount,
            'order_count': order_count,
            'customers': customers,
            'no_deliverd': no_deliverd,
            'no_cancel': no_cancel,
            'no_return': no_return,
            'monthly_sales_data': monthly_sales_data
        }
        return render(request, 'adminside/dashboard/index.html', context)
    else:
        return redirect('admin_login')
    # return render(request, 'adminside/dashboard/index.html')


def UsersDetails(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        users = CustomUser.objects.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        ).filter(is_superuser=False).order_by('id')
        user_count = CustomUser.objects.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        ).filter(is_superuser=False).order_by('id').count()
    else:
        users = CustomUser.objects.filter(is_superuser=False).order_by('id')
        user_count = CustomUser.objects.filter(is_superuser=False).order_by('id').count()

    paginator = Paginator(users, 6)
    page_number = request.GET.get('page', 1)
    users = paginator.get_page(page_number)
    context = {
        'users': users,
        'user_count': user_count

    }
    return render(request, 'adminside/users/users_details.html', context)


def UserBlock(request, user_id):

    user = CustomUser.objects.get(id=user_id)
    if user.is_active:
        user.is_active = False
        user.save()
        users = CustomUser.objects.filter(is_superuser=False).order_by('id')
        context = {
            'users': users
        }
        return render(request, 'adminside/users/users_details.html', context)
    else:
        user.is_active = True
        user.save()
        users = CustomUser.objects.filter(is_superuser=False).order_by('id')
        context = {
            'users': users
        }
        return render(request, 'adminside/users/users_details.html', context)


def get_sales_revenue(request):
    # Replace this with your actual data retrieval logic
    # Example mock data
    data = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'sales': [100, 200, 150, 300, 250, 400],
        'revenue': [500, 600, 550, 700, 650, 800],
    }

    return JsonResponse(data)