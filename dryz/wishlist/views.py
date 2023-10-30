from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from carts.views import add_cart
from product.models import ProductVariant
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

from wishlist.models import Wishlist
from django.contrib import messages

# Create your views here.


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist': wishlist,
    }
    return render(request,'user/wishlist/wishlist.html',context)
def add_whishlit(request,variant_id):
    variant = ProductVariant.objects.get(id=variant_id)
    try:
        is_exist = Wishlist.objects.filter(user=request.user, variant=variant).exists()

        if is_exist:
            # Wishlist item already exists
            messages.error(request, 'This product is already in your wishlist.')
        else:
            # Wishlist item does not exist, add it
            wishlist = Wishlist(user=request.user, variant=variant)
            wishlist.save()
            messages.success(request, 'Product added to wishlist.')

        return redirect('home')

    except Exception as e:
        # Handle exceptions if any
        # Log or handle the exception accordingly
        print(e)
        messages.error(request, 'Failed to add the product to the wishlist.')
        return redirect('home')


def remove_wish_list(request,wish_id):

    try:
        # Find the wishlist item
        wishlist_item = Wishlist.objects.get(id=wish_id, user=request.user)
        wishlist_item.delete()  # Remove the wishlist item
    except Wishlist.DoesNotExist:
        pass
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist': wishlist,
    }
    return render(request, 'user/wishlist/wishlist.html', context)


def add_wish_to_cart(request,wish_id):
    try:
        # Find the wishlist item
        wishlist_item = Wishlist.objects.get(id=wish_id, user=request.user)
        add_cart(request,product_id= wishlist_item.variant.id)
        wishlist_item.delete()  # Remove the wishlist item
    except Wishlist.DoesNotExist:
        pass
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist': wishlist,
    }
    return render(request, 'user/wishlist/wishlist.html', context)

    # return render(request, 'user/wishlist/wishlist.html', context)
    # return HttpResponse("hjks")