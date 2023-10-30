from accounts.models import CustomUser


def wallet(request):
    wallet = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            email=request.user
            user = CustomUser.objects.get(email=email)
            wallet = user.wallet
        except:
            wallet = 0
    return dict(wallet=wallet)

