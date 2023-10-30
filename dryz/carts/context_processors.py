from accounts.models import CustomUser
from .models import Cart,CartItem
from .views import _cart_id


def counter(request):
    cart_count=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart_id = _cart_id(request)
            cart = Cart.objects.filter(cart_id=cart_id)
            try:
                email=request.session['user-email']
                user=CustomUser.objects.get(email=email)
                # print("8888888888888888888888888888888888", user)
                cart_items = CartItem.objects.filter(user=user)
            except:
                cart_items=CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count=0
    return dict(cart_count=cart_count)

