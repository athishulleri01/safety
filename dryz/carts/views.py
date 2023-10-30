from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View

from accounts.models import CustomUser
from carts.models import Cart, CartItem, Address
from order.models import Order, OrderItem, Coupon
from product.models import Product, ProductVariant
import random
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.db.models import Q
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from django.conf import settings


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    variant = ProductVariant.objects.get(id=product_id)
    product = Product.objects.get(id=variant.product.id)  # Get the product
    if request.method == 'POST':
        weight = request.POST.get('variant')
        weightt = request.POST.get('weightt')
        product_id = request.POST.get('product_id')
        variant_id = request.POST.get('variant_id')

        try:
            variation = ProductVariant.objects.get(id=variant_id)
            product = Product.objects.get(id=variation.product.id)
            cart_id = _cart_id(request)  # Get or generate the cart_id
            try:
                cart = Cart.objects.get(cart_id=cart_id)  # Get the cart using the cart_id
            except Cart.DoesNotExist:
                cart = Cart.objects.create(
                    cart_id=cart_id
                )
            try:
                try:
                    email = request.session['user-email']
                    user = CustomUser.objects.get(email=email)
                    if user is not None:
                        cart_item = CartItem.objects.get(product=product, variant=variation, cart=cart)
                    else:
                        cart_item = CartItem.objects.get(product=product, variant=variation, cart=cart)
                except:
                    cart_item = CartItem.objects.get(product=product, variant=variation, cart=cart)
                # print(type(cart_item.variant.weight),type(weightt),cart_item.variant.weight,weightt)
                if cart_item.variant.weight == float(weightt):
                    cart_item.quantity += 1  # Increment the quantity of the existing cart item
                else:
                    cart_item = CartItem.objects.create(
                        product=product,
                        quantity=1,
                        cart=cart,
                        variant=variation,
                    )


            except CartItem.DoesNotExist:
                try:
                    if user is not None:
                        cart_item = CartItem.objects.create(
                            product=product,
                            quantity=1,
                            cart=cart,
                            variant=variation,
                            user=user
                        )
                except:
                    cart_item = CartItem.objects.create(
                        product=product,
                        quantity=1,
                        cart=cart,
                        variant=variation,

                    )
                cart_item.save()

            cart_item.save()  # Save the cart item
            return redirect('cart')

        except:
            return HttpResponse("not working")
    else:
        try:
            cart_id = _cart_id(request)  # Get or generate the cart_id
            try:
                cart = Cart.objects.get(cart_id=cart_id)  # Get the cart using the cart_id
            except Cart.DoesNotExist:
                cart = Cart.objects.create(
                    cart_id=cart_id
                )
            try:
                try:
                    email = request.session['user-email']
                    user = CustomUser.objects.get(email=email)
                    if user is not None:
                        cart_item = CartItem.objects.get(product=product, variant=variant, cart=cart)
                    else:
                        cart_item = CartItem.objects.get(product=product, variant=variant, cart=cart)
                except:
                    cart_item = CartItem.objects.get(product=product, variant=variant, cart=cart)
                # print(type(cart_item.variant.weight),type(weightt),cart_item.variant.weight,weightt)
                if cart_item.variant.id == product_id:
                    cart_item.quantity += 1  # Increment the quantity of the existing cart item
                else:
                    cart_item = CartItem.objects.create(
                        product=product,
                        quantity=1,
                        cart=cart,
                        variant=variant,
                    )


            except CartItem.DoesNotExist:
                try:
                    if user is not None:
                        cart_item = CartItem.objects.create(
                            product=product,
                            quantity=1,
                            cart=cart,
                            variant=variant,
                            user=user
                        )
                except:
                    cart_item = CartItem.objects.create(
                        product=product,
                        quantity=1,
                        cart=cart,
                        variant=variant,

                    )
                cart_item.save()

            cart_item.save()  # Save the cart item
            return redirect('cart')

        except:
            return HttpResponse("not working")

    return redirect('cart')

# cart = CartItem.objects.get(variant=variant).exists()
#         print(cart,"kkkkkkkkkkkkkkkkkk")
def cart(request, total=0, quantity=0, cart_items=None):
    cart_id = _cart_id(request)
    tax = 0
    grand_total = 0
    current_date = timezone.now()
    if request.method == 'POST':

        try:
            try:
                email = request.session['user-email']
                user = CustomUser.objects.get(email=email)
                if user is not None:
                    cart_items = CartItem.objects.filter(user=user, is_active=True).order_by('id')
            except:
                cart = Cart.objects.get(cart_id=cart_id)
                cart_items = CartItem.objects.filter(cart=cart, is_active=True).order_by('id')

            coupon_select = request.POST.get('coupon_select')
            valid_coupons = Coupon.objects.get(
                Q(coupon_code=coupon_select) &
                Q(start_date__lte=current_date) &
                Q(end_date__gte=current_date) &
                Q(active=True)
            )

            for cart_item in cart_items:
                total += (cart_item.variant.selling_price * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2 * total) / 100
            grand_total = total + tax
            if total > valid_coupons.min_purchase:
                request.session['coupon'] = valid_coupons.coupon_discount
                total = total - valid_coupons.coupon_discount
            else:
                valid_coupon = Coupon.objects.filter(
                    Q(start_date__lte=current_date) &
                    Q(end_date__gte=current_date) &
                    Q(active=True)
                )
                messages.error(request, f'This Coupon only applicable for minimum amount{valid_coupons.min_purchase}')
                context = {
                    'total': total,
                    'quantity': quantity,
                    'cart_items': cart_items,
                    'tax': tax,
                    'grand_total': grand_total,
                    'valid_coupons': valid_coupon

                }
                return render(request, 'user/cart/cart.html', context)
        except ObjectDoesNotExist:
            pass
        valid_coupons = None
        context = {
            'total': total,
            'quantity': quantity,
            'cart_items': cart_items,
            'tax': tax,
            'grand_total': grand_total,
            'valid_coupons': valid_coupons

        }
        return render(request, 'user/cart/cart.html', context)

    # Get or generate the
    else:

        try:
            try:
                email = request.session['user-email']
                user = CustomUser.objects.get(email=email)
                if user is not None:
                    cart_items = CartItem.objects.filter(user=user, is_active=True).order_by('id')
            except:
                cart = Cart.objects.get(cart_id=cart_id)
                cart_items = CartItem.objects.filter(cart=cart, is_active=True).order_by('id')
            for cart_item in cart_items:
                total += (cart_item.variant.selling_price * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2 * total) / 100
            grand_total = total + tax
        except ObjectDoesNotExist:
            pass

        valid_coupons = Coupon.objects.filter(
            Q(start_date__lte=current_date) &
            Q(end_date__gte=current_date) &
            Q(active=True)
        )
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'valid_coupons': valid_coupons

    }
    return render(request, 'user/cart/cart.html', context)


def remove(request, product_id):
    cart_id = _cart_id(request)  # Get or generate the cart_id
    productvariant = get_object_or_404(ProductVariant, id=product_id)
    print(productvariant)
    try:
        email = request.session['user-email']
        user = CustomUser.objects.get(email=email)
        cart_item = CartItem.objects.get(variant=productvariant, user=user)
    except:
        cart = Cart.objects.get(cart_id=cart_id)
        cart_item = CartItem.objects.get(variant=productvariant, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        total = cart_item.quantity * cart_item.variant.selling_price
        return JsonResponse({'quantity': cart_item.quantity, 'total': total})
    else:
        cart_item.delete()
        return JsonResponse({'status': 'empty'})


def adding(request, product_id):
    cart_id = _cart_id(request)  # Get or generate the cart_id
    productvariant = get_object_or_404(ProductVariant, id=product_id)
    try:
        email = request.session['user-email']
        user = CustomUser.objects.get(email=email)
        cart_item = CartItem.objects.get(variant=productvariant, user=user)
    except:
        cart = Cart.objects.get(cart_id=cart_id)
        cart_item = CartItem.objects.get(variant=productvariant, cart=cart)
    # if cart_item.quantity > 1:
    cart_item.quantity += 1
    cart_item.save()
    total = cart_item.quantity * cart_item.variant.selling_price
    return JsonResponse({'quantity': cart_item.quantity, 'total': total})


def remove_cart_item(request, product_id):
    cart_id = _cart_id(request)  # Get or generate the cart_id
    productvariant = get_object_or_404(ProductVariant, id=product_id)
    try:
        email = request.session['user-email']
        user = CustomUser.objects.get(email=email)
        cart_item = CartItem.objects.get(variant=productvariant, user=user)
    except:
        cart = Cart.objects.get(cart_id=cart_id)
        cart_item = CartItem.objects.get(variant=productvariant, cart=cart)
    cart_item.delete()
    return redirect('cart')


# user profile
@login_required(login_url='user_signin')
def profile(request):
    if request.method == 'POST':
        email = request.session['user-email']
        user = CustomUser.objects.get(email=email)
        username = request.POST.get('username')
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "username already exist..!")
        else:
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.phone = request.POST.get('phone')
            user.first_name = request.POST.get('firstname')
            user.last_name = request.POST.get('lastname')
            user.save()
    if 'user-email' in request.session:
        email = request.user
        user = CustomUser.objects.get(email=email)
        context = {
            'user': user
        }
        return render(request, 'user/user-profile/profile.html', context)
    return redirect('user_signin')


# address
@login_required(login_url='user_signin')
def address(request):
    if 'user-email' in request.session:
        email = request.session['user-email']
        user = CustomUser.objects.get(email=email)
        addresses = Address.objects.filter(user_id=user)
        context = {
            'addresses': addresses
        }
        return render(request, 'user/user-profile/address.html', context)

    return render(request, 'user/user-profile/address.html')


@login_required(login_url='user_signin')
def edit_address(request, address_id):
    if request.method == 'POST':
        address = Address.objects.get(id=address_id)
        address.recipient_name = request.POST.get('RecipientName')
        address.email = request.POST.get('email')
        address.house_no = request.POST.get('house_no')
        address.phone = request.POST.get('phone')
        address.street_name = request.POST.get('street_name')
        address.village_name = request.POST.get('Village')
        address.postal_code = request.POST.get('postal_code')
        address.district = request.POST.get('district')
        address.state = request.POST.get('state')
        address.country = request.POST.get('country')
        default_address = request.POST.get('default_address')
        if default_address == 'on':
            try:
                email = request.user
                user = CustomUser.objects.get(email=email)
                adrss = Address.objects.get(user_id=user, is_default=True)
                print(adrss)
                adrss.is_default = False
                print(adrss.is_default)
                adrss.save()
            except Address.DoesNotExist:
                pass
        address.is_default=True
        address.save()
        addresses = Address.objects.filter(user_id=address.user_id)
        context = {
            'addresses': addresses
        }
        return render(request, 'user/user-profile/address.html', context)
    return render(request, 'user/user-profile/address.html')


@login_required(login_url='user_signin')
def add_address(request):
    email = request.session['user-email']
    user = CustomUser.objects.get(email=email)
    default_address = request.POST.get('default_address')
    if default_address == 'on':
        try:
            adrss = Address.objects.get(user_id=user, is_default=True)
            print(adrss)
            adrss.is_default = False
            print(adrss.is_default)
            adrss.save()
        except Address.DoesNotExist:
            pass
    address = Address()
    address.user_id = user
    address.recipient_name = request.POST.get('RecipientName')
    address.email = request.POST.get('email')
    address.house_no = request.POST.get('house_no')
    address.phone = request.POST.get('phone')

    address.is_default = True
    address.street_name = request.POST.get('street_name')
    address.village_name = request.POST.get('Village')
    address.postal_code = request.POST.get('postal_code')
    address.district = request.POST.get('district')
    address.state = request.POST.get('state')
    address.country = request.POST.get('country')
    address.save()
    addresses = Address.objects.filter(user_id=user)
    context = {
        'addresses': addresses
    }
    return render(request, 'user/user-profile/address.html', context)


@login_required(login_url='user_signin')
def delete_address(request, address_id):
    address = Address.objects.get(id=address_id)
    if address is not None:
        address.delete()
        return redirect('address')


@login_required(login_url='user_signin')
def checkout(request):
    if request.method == 'POST':
        email = request.session['user-email']
        user = CustomUser.objects.get(email=email)
        recipient_name = request.POST.get('username')
        selected_address_id = request.POST.get('selectedAddress')
        if recipient_name is None:
            address = Address.objects.get(id=selected_address_id)
        else:
            address = Address.objects.get(recipient_name=recipient_name)

        order = Order()
        order.user = user
        order.address = address
        cart = CartItem.objects.filter(user=user, is_active=True)
        cart_total_price = 0
        for item in cart:
            cart_total_price = (cart_total_price + item.variant.selling_price
                                * item.quantity)

        trackno = 'pvkewt' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'pvkewt' + str(random.randint(1111111, 9999999))
        order.tracking_no = trackno
        try:
            if request.session['coupon']:
                offer = request.session['coupon']
        except:
            offer = None
        payment_mode = request.POST.get('payment_mode')
        if payment_mode == 'Paid by Razorpay':
            if offer is not None:
                offer = request.session['coupon']
                order.total_price = cart_total_price - offer
            else:
                order.total_price = cart_total_price
            order.payment_mode = request.POST.get('payment_mode')
            order.payment_id = request.POST.get('payment_id')
        elif payment_mode == 'wallet':
            users = CustomUser.objects.get(email=email)
            wallet = users.wallet
            if offer is not None:
                offer = request.session['coupon']
                total_price = (wallet - cart_total_price)
                order.total_price = total_price-offer
                wallet =users.wallet -total_price
                users.wallet = wallet -offer
            else:
                order.total_price = wallet - cart_total_price
                users.wallet = wallet - cart_total_price
            users.save()
            order.payment_mode = 'wallet'
            order.payment_id = ' '
        else:
            if offer is not None:
                offer = request.session['coupon']
                order.total_price = cart_total_price - offer

            else:
                order.total_price = cart_total_price
            order.payment_mode = 'cod'
            order.payment_id = ' '
        order.save()

        neworderitems = CartItem.objects.filter(user=user, is_active=True)
        for item in neworderitems:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                variant=item.variant,
                price=item.variant.selling_price,
                quantity=item.quantity,
                user=user
            )
            # reduce the product quantity from available stock
            orderproduct = ProductVariant.objects.filter(
                id=item.variant.id
                ).first()
            orderproduct.stock = orderproduct.stock - item.quantity
            orderproduct.save()
        Cart.objects.filter(cart_id= item.cart.cart_id).delete()

        payMode = request.POST.get('payment')
        if payMode == 'Paid by Razorpay':
            order_status = order.status
            return JsonResponse({
                'status': 'Your order has been placed successfully',
                'order': f"{order_status}",
                'cart_items': 'athii'
            }, content_type='application/json')
        elif payMode == 'wallet':
            order_status = order.status
            return JsonResponse({
                'status': 'Your order has been placed successfully',
                'order': f"{order_status}",
                'cart_items': 'manu'
            }, content_type='application/json')
        else:
            # invoice = GenerateInvoice()
            # invoice.get(request,pk=order.id)
            template = get_template('user/order/invoice_download.html')

            cont = {
                'order': order,
                'cart_items': neworderitems
            }
            html = template.render(cont)
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)  # , link_callback=fetch_resources)
            pdf = result.getvalue()
            filename = 'Invoice_' + str(cont['order']) + '.pdf'
            subject = f"Hello, {order.user.username}!"
            message = "invoice - order conformation"
            email = EmailMultiAlternatives(
                subject,
                message,  # necessary to pass some message here
                'dryzz.official@gmail.com',
                [order.address.email]
            )
            email.attach_alternative(html, "text/html")
            email.attach(filename, pdf, 'application/pdf')
            email.send(fail_silently=False)

            return render(request, 'user/order/order_page.html', cont)
        # return redirect('home')

    if 'user-email' in request.session:
        cart_id = _cart_id(request)  # Get or generate the cart_id
        tax = 0
        grand_total = 0
        total = 0
        quantity = 0
        cart_items = ''
        try:

            try:
                email = request.session['user-email']
                user = CustomUser.objects.get(email=email)
                cart_items = CartItem.objects.filter(user=user, is_active=True)
            except:
                cart = Cart.objects.get(cart_id=cart_id)
                cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for cart_item in cart_items:
                total += (cart_item.variant.selling_price * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2 * total) / 100
            grand_total = total + tax

        except ObjectDoesNotExist:
            pass
        try:
            email = request.session['user-email']
            user = CustomUser.objects.get(email=email)
            addresses = Address.objects.filter(user_id=user, is_default=False)
        except:
            pass
        try:
            default_address = Address.objects.get(user_id=user, is_default=True)
        except:
            default_address = Address.objects.filter(user_id=user).first()
        try:
            if request.session['coupon']:
                offer = request.session['coupon']
                total = total - offer
        except:
            pass
        context = {
            'total': total,
            'quantity': quantity,
            'cart_items': cart_items,
            'addresses': addresses,
            'grand_total': grand_total,
            'default_address': default_address,

        }
        return render(request, 'user/checkout/checkout.html', context)
    return redirect('user_signin')


def pdf_download(request,id):
    order=Order.objects.get(id=id)
    neworderitems=OrderItem.objects.filter(order=order)
    cont = {
        'order': order,
        'cart_items': neworderitems
    }
    pdf = render_to_pdf('user/order/invoice_download.html', cont)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % (cont['order'])
        content = "inline; filename='%s'" % (filename)
        # download = request.GET.get("download")
        # if download:
        content = "attachment; filename=%s" % (filename)
        response['Content-Disposition'] = content
        return response

@login_required(login_url='user_signin')
def add_address_checkout(request):
    email = request.session['user-email']
    user = CustomUser.objects.get(email=email)
    address = Address()
    address.user_id = user
    address.recipient_name = request.POST.get('RecipientName')
    address.email = request.POST.get('email')
    address.house_no = request.POST.get('house_no')
    address.street_name = request.POST.get('street_name')
    address.village_name = request.POST.get('Village')
    address.postal_code = request.POST.get('postal_code')
    address.district = request.POST.get('district')
    address.state = request.POST.get('state')
    address.phone = request.POST.get('phone')
    address.country = request.POST.get('country')
    address.save()
    # addresses = Address.objects.filter(user_id=user)
    return redirect('checkout')


@login_required(login_url='user_signin')
def selectedAddress(request):
    if request.method == 'GET':
        selected_option = request.GET.get('selectedOption')
        address = Address.objects.get(id=selected_option)
        print(selected_option)
        response_data = {
            'username': address.recipient_name,
            'email': address.email,
            'phone': address.phone,
            'house_no': address.house_no,
            'street': address.street_name,
            'district': address.district,
            'state': address.state,
            'country': address.country,
            'pincode': address.postal_code
        }
        return JsonResponse(response_data)


@login_required(login_url='user_signin')
def order(request, id=None):
    try:
        if request.session['coupon']:
            offer = request.session['coupon']
    except:
        offer = None
    total = 0
    if id:
        order = Order.objects.get(payment_id=id)
        print(order.payment_mode)
        neworderitems = OrderItem.objects.filter(order=order.id)
        print(neworderitems)
        for item in neworderitems:
            total = total + item.variant.selling_price
        if offer is not None:
            total = total - offer
            del request.session['coupon']
        context = {
            'order': order,
            'cart_items': neworderitems,
            'total': total
        }
        return render(request, 'user/order/order_page.html', context)
    email=request.user
    print(email)
    user=CustomUser.objects.get(email=email)
    order = Order.objects.filter(user=user).latest('id')
    neworderitems = OrderItem.objects.filter(order=order)

    for item in neworderitems:
        total = total + item.variant.selling_price
    if offer is not None:
        offer = request.session['coupon']
        total = total - offer
        del request.session['coupon']
    context = {
        'order': order,
        'cart_items': neworderitems,
        'total': total
    }
    return  render(request, 'user/order/order_page.html', context)




# for generating pdf invoice
def fetch_resources(uri, rel):
    path = os.path.join(uri.replace(settings.STATIC_URL, ""))
    return path


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class GenerateInvoice(View):
    def get(self, request, pk, *args, **kwargs):
        try:
            order = Order.objects.get(payment_id=id)
            neworderitems = OrderItem.objects.filter(order=order.id)
        except:
            return HttpResponse("505 Not Found")
        data = {
            'order': order,
            'cart_items': neworderitems
        }
        pdf = render_to_pdf('user/order/order_page.html', data)
        # return HttpResponse(pdf, content_type='application/pdf')

        # force download
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" % (order.id)
            content = "inline; filename='%s'" % (filename)
            # download = request.GET.get("download")
            # if download:
            content = "attachment; filename=%s" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")