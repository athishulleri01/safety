from accounts.models import CustomUser
from .models import Wishlist


def wishlist(request):
    wishlist=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            email = request.user
            user = CustomUser.objects.get(email=email)
            wishlist = Wishlist.objects.filter(user=user).count()
        except:
            cart_count=0
    return dict(wish_count=wishlist)

