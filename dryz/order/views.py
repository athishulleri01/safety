from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from accounts.models import CustomUser
from carts.models import CartItem
from carts.views import render_to_pdf
from order.models import Order, OrderItem, ReturnOrder, Coupon
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
# Create your views here.


def ViewCoupons(request):
    coupons = Coupon.objects.all().order_by('-id')
    context = {
        'coupons': coupons
    }
    return render(request, 'adminside/coupon/view_coupon.html',context)


def add_coupon(request):
    if request.method == 'POST':
        coupon = Coupon()
        coupon.coupon_name=request.POST.get('coupon_name')
        coupon.coupon_code = request.POST.get('coupon_code')
        coupon.min_purchase=request.POST.get('min_price')
        coupon.coupon_discount = request.POST.get('discount_amount')
        coupon.start_date=request.POST.get('start_date')
        coupon.end_date=request.POST.get('end_date')
        coupon.save()
        return redirect('view_coupons')

def edit_coupon(request,id):
    if request.method == 'POST':
        coupon = Coupon.objects.get(id=id)
        coupon.coupon_name = request.POST.get('coupon_name')
        coupon.coupon_code = request.POST.get('coupon_code')
        coupon.min_purchase = request.POST.get('min_price')
        coupon.coupon_discount = request.POST.get('discount_amount')
        coupon.start_date = request.POST.get('start_date')
        coupon.end_date = request.POST.get('end_date')
        coupon.save()
        return redirect('view_coupons')
def delete_coupon(request,id):
    coupons = Coupon.objects.get(id=id)
    coupons.delete()
    return redirect('view_coupons')
def razorpaycheck(request):
    email = request.session['user-email']
    user = CustomUser.objects.get(email=email)
    cart = CartItem.objects.filter(user=user)
    total_price = 0
    for item in cart:
        total_price = total_price + item.variant.selling_price * item.quantity
    try:
        if request.session['coupon']:
            offer = request.session['coupon']
            total_price = total_price - offer
    except:
        pass
    return JsonResponse({
        'total_price': total_price
    })


def wallet_payment(request):
    print("<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>")
    email = request.session['user-email']
    user = CustomUser.objects.get(email=email)
    cart = CartItem.objects.filter(user=user)
    total_price = 0
    for item in cart:
        total_price = total_price + item.variant.selling_price * item.quantity
    return JsonResponse({
        'total_price': total_price
    })

def view_orders_admin(request):
    if request.method=="POST":
        status=request.POST.get('status')
        print(status)
        if status == 'status' or status == 'all':
            orders = Order.objects.all().order_by('-id')
        else:
            orders = Order.objects.filter(status=status).order_by('-id')
        context = {
            'orders': orders
        }
        return render(request, 'adminside/order/view_order_admin.html', context)
    try:
        orders = Order.objects.all().order_by('-id')
        context = {
            'orders': orders
        }
        return render(request, 'adminside/order/view_order_admin.html', context)

    except:
        pass


def view_single_order_admin(request, order_id):
    order = Order.objects.get(id=order_id)
    order_item = OrderItem.objects.filter(order=order)
    order_return_message = ReturnOrder.objects.filter(order=order).first()
    user=CustomUser.objects.get(id=order.user.id)
    # user.wallet = user.wallet+order.total_price
    user.save()
    context = {
        'order': order,
        'order_item': order_item,
        # 'order_return_message': order_return_message
    }
    return render(request, 'adminside/order/view_single_order_admin.html', context)


def order_status(request):
    print("[[[[[")
    if request.method == 'POST':
        try:
            order_id = request.POST.get('order_id')
            order_status = request.POST.get('order_status')
            print(order_status)
            if order_status == 'Order Status':
                order = Order.objects.get(id=order_id)
                order_item = OrderItem.objects.filter(order=order)
                context = {
                    'order': order,
                    'order_item': order_item
                }
                return render(request, 'adminside/order/view_single_order_admin.html', context)
            order = Order.objects.get(id=order_id)
            order_item = OrderItem.objects.filter(order=order)
            for item in order_item:
                item.status = order_status
                item.save()
            order.status = order_status
            order.save()
            if order_status == 'Returned':
                email = order.user.email
                user = CustomUser.objects.get(email=email)
                print("////////////////")
                print(user.wallet)
                user.wallet = user.wallet + order.total_price
                print(user.wallet)
                user.save()
            order_item = OrderItem.objects.filter(order=order)
            context = {
                'order': order,
                'order_item': order_item
            }
            return render(request, 'adminside/order/view_single_order_admin.html', context)
        except:
            pass

    order_item = OrderItem.objects.filter(order=order)
    context = {
        'order': order,
        'order_item': order_item
    }
    return render(request, 'adminside/order/view_single_order_admin.html', context)


def return_approval(request,order_id):
    order = Order.objects.get(id=order_id)
    order.status = 'Returned'
    order.save()
    order_item = OrderItem.objects.filter(order=order)
    for item in order_item:
        item.status = 'Returned'
        item.save()
    context = {
        'order': order,
        'order_item': order_item
    }
    return render(request, 'adminside/order/view_single_order_admin.html', context)


def view_orders_user(request):
    email = request.user
    user = CustomUser.objects.get(email=email)
    if request.method == "POST":
        status=request.POST.get('status')
        order = Order.objects.filter(user=user)
        if status == 'status' or status == 'all':
            order_items = OrderItem.objects.filter(user=user).order_by('-id')
        else:
            print(status)
            order_items = OrderItem.objects.filter(user=user,status=status).order_by('-id')
            order_items1 = OrderItem.objects.filter(user=user, status='Cancelled').values()
            print(order_items1)
        context = {
            "order": order,
            "order_items": order_items
        }
    else:
        order = Order.objects.filter(user=user)
        order_items = OrderItem.objects.filter(user=user).order_by('-id')
        context = {
            "order": order,
            "order_items": order_items
        }
    return render(request, 'user/user-profile/order.html', context)


def track_order_status(request, order_item_id):
    order_item = OrderItem.objects.get(id=order_item_id)
    order=Order.objects.get(id=order_item.order.id)
    orders =  OrderItem.objects.filter(order=order)
    orderstatus = order_item.status
    print(orderstatus)
    context = {
        'status': orderstatus,
        'item': order_item,
        'order': order,
        'orders': orders
    }

        # return redirect(reverse('view_images', args=[product.id]))
    return render(request,'user/user-profile/track_order.html', context)


def cancel_order(request,order_item_id):
    order_item = OrderItem.objects.get(id=order_item_id)
    order = Order.objects.get(id=order_item.order.id)
    if request.method == 'POST':
        order.status = 'Cancelled'
        order.save()
        order_items = OrderItem.objects.filter(order=order)
        print(order.payment_mode)
        if order.payment_mode == 'Paid by Razorpay' or order.payment_mode == 'wallet':
            email = request.user
            user = CustomUser.objects.get(email=email)
            user.wallet = user.wallet + int(order.total_price)
            user.save()
        for item in order_items:
            reason = request.POST.get('cancel')
            item.status = 'Cancelled'
            item.save()
        return redirect('view_orders_user')


def return_order(request, order_item_id):
    order_item = OrderItem.objects.get(id=order_item_id)
    order = Order.objects.get(id=order_item.order.id)
    if request.method == 'POST':
        reason = request.POST.get('reason')
        returnorder = ReturnOrder()
        returnorder.order_item = order_item
        returnorder.order = order
        returnorder.return_comment = reason
        returnorder.save()

        order_items = OrderItem.objects.filter(order=order)
        for item in order_items:
            reason = request.POST.get('return')
            item.status = 'Return requested'
            item.save()
            order.status = "Return requested"
            order.save()

        return redirect('view_orders_user')


def sales_report(request):
    total_sales = 0
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        orders = Order.objects.filter(created_at__range=(start_date, end_date))
        total_order = Order.objects.filter(created_at__range=(start_date, end_date)).count()
        Pending = Order.objects.filter(created_at__range=(start_date, end_date),status='Order confirmed').count()
        Processing = Order.objects.filter(created_at__range=(start_date, end_date),status="In Production").count()
        Shipped = Order.objects.filter(created_at__range=(start_date, end_date),status='Shipped').count()
        Delivered = Order.objects.filter(created_at__range=(start_date, end_date),status='Delivered').count()
        cancelled = Order.objects.filter(created_at__range=(start_date, end_date),status='Cancelled').count()
        Return = Order.objects.filter(created_at__range=(start_date, end_date),status='Returned').count()
        for order in orders:
            total_sales = total_sales + order.total_price
    else:

        orders = Order.objects.all()
        total_order = Order.objects.all().count()
        Pending = Order.objects.filter(status='Order confirmed').count()
        Processing = Order.objects.filter(status="In Production").count()
        Shipped = Order.objects.filter(status='Shipped').count()
        Delivered = Order.objects.filter(status='Delivered').count()
        cancelled = Order.objects.filter(status='Cancelled').count()
        Return = Order.objects.filter(status='Returned').count()
        for order in orders:
            total_sales = total_sales + order.total_price

    context = {
        'orders': orders,
        'total_sales': total_sales,
        'total_order': total_order,
        'Pending': Pending,
        'Processing': Processing,
        'Shipped': Shipped,
        "Delivered": Delivered,
        'cancelled': cancelled,
        'Return': Return
    }
    return render(request, 'adminside/sales_report/view_sales_report.html', context)


def render_to_pdf(template_path, context_dict):
    template = get_template(template_path)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Sales_report.pdf"'

    # Create a PDF with xhtml2pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def sales_report_pdf_download(request):
    order = Order.objects.all()
    cont = {
        'orders': order,
    }
    pdf = render_to_pdf('adminside/sales_report/sales_report_download.html', cont)
    return pdf
