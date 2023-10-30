from django.http import HttpResponse
from django.shortcuts import render

from accounts.models import CustomUser
from categories.models import Category, Sub_Category
from product.models import Product, ProductVariant, ReviewRating
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.
def home(request):
    cat = Category.objects.filter(is_visible=True)
    sub_cat = Sub_Category.objects.filter(is_visible=True)
    products = Product.objects.filter(is_visible=True)

    products_with_default_variants = Product.objects.prefetch_related('variants').filter(
        variants__is_available=True)
    product_queryset = ProductVariant.objects.none()
    for product in products_with_default_variants:
        default_variant = product.variants.filter(is_available=True).first()
        if default_variant:
            product_queryset |= ProductVariant.objects.filter(pk=default_variant.pk)


    context = {
        'category': cat,
        'sub_category': sub_cat,
        'products': product_queryset,
        'newest_products': product_queryset,
        'top_rated_products': product_queryset
    }
    return render(request, 'user/home/home.html', context)


def error_404_view(request, exception):
    return render(request, 'include/404page.html')


import re


def remove_currency_symbols(input_string):
    # Define a regular expression pattern to match dollar ($) and rupee (₹) symbols
    currency_symbols = r'[$₹]'

    # Use the sub() function from the re module to replace the currency symbols with an empty string
    output_string = re.sub(currency_symbols, '', input_string)

    return output_string

from django.db.models import QuerySet
def ViewShop(request):
    if request.method == 'POST':
        minamount = int(remove_currency_symbols(request.POST.get('minamount')))
        maxamount = int(remove_currency_symbols(request.POST.get('maxamount')))
        filter_weight = request.POST.get('filter_weight')
        print(minamount,maxamount,filter_weight)

        if minamount and minamount and filter_weight!= None:
            print("hooo")
            products_within_price_range = ProductVariant.objects.filter(selling_price__gte=minamount,
                                                                 selling_price__lte=maxamount,weight=filter_weight)
        else:
            products_within_price_range = ProductVariant.objects.filter(selling_price__gte=minamount,
                                                                        selling_price__lte=maxamount)
        paginator = Paginator(products_within_price_range, 6)
        page_number = request.GET.get('page', 1)
        products_within_price_range = paginator.get_page(page_number)
        sub_cat = Sub_Category.objects.filter(is_visible=True)
        context = {
            'products': products_within_price_range,
            'all_products': products_within_price_range,
            'sale_off': products_within_price_range,
            'sub_category': sub_cat,
        }
        return render(request, 'user/shop/shop.html', context)

    else:
        products_with_default_variants = Product.objects.prefetch_related('variants').filter(
            variants__is_available=True)
        product_queryset = ProductVariant.objects.none()
        for product in products_with_default_variants:
            default_variant = product.variants.filter(is_available=True).first()
            if default_variant:
                product_queryset |= ProductVariant.objects.filter(pk=default_variant.pk)
        sub_cat = Sub_Category.objects.filter(is_visible=True)
        paginator = Paginator(product_queryset, 6)
        page_number = request.GET.get('page', 1)
        product_queryset = paginator.get_page(page_number)
        context = {
            'products': product_queryset,
            'all_products': product_queryset,
            'sale_off': product_queryset,
            'sorted_product': product_queryset,
            'sub_category': sub_cat,

        }
        return render(request, 'user/shop/shop.html', context)


def Search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=keyword) | 
                Q(product_name__icontains=keyword))
    newest_products = Product.objects.all().order_by('-created_date')[:10]
    top_rated_products = Product.objects.all().order_by('created_date')[:10]
    sub_cat = Sub_Category.objects.all()

    context = {
        'products': products,
        'newest_products': newest_products,
        'top_rated_products': top_rated_products,
        'sub_category': sub_cat,

    }
    return render(request, 'user/home/home.html', context)