import os

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import CustomUser
from carts.models import CartItem
from carts.views import _cart_id
from categories.models import Sub_Category, Category
from order.models import OrderItem
from .forms import ReviewForm
from .models import Product, ProductVariant, ProductImage, ReviewRating
from decimal import Decimal
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from dryz import settings
from django.contrib import messages


# Create your views here.
def ViewProducts(request):
    products = Product.objects.filter(is_visible=True).order_by('id')
    sub_cat = Sub_Category.objects.filter(is_visible=True).order_by('id')

    paginator = Paginator(products, 3)
    page_number = request.GET.get('page', 1)
    products = paginator.get_page(page_number)
    context = {
        'products': products,
        'sub_cat': sub_cat,

    }

    return render(request, 'adminside/product/view_products.html', context)


def AddProduct(request):
    product = Product()
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product.product_name = request.POST.get('product_name')
        product.slug = product_name.replace(" ", "-")
        product.description = request.POST.get('description')
        sub_category = request.POST.get('category_name')
        sub_cat = Sub_Category.objects.get(id=sub_category)
        product.sub_category = sub_cat
        product.category = sub_cat.category
        product.original_price = 0.0
        product.selling_prince = 0.0
        images = request.FILES.getlist('images')
        if images:
            product.images = images[len(images) - 1]

        variant_weights = request.POST.getlist("variant_weight[]")
        original_prices = request.POST.getlist("variant_original_price[]")
        selling_prices = request.POST.getlist("variant_selling_price[]")
        stocks = request.POST.getlist('variant_stock[]')
        unit = request.POST.getlist('unit[]')

        for weight, original_price, selling_price, stock, unit in zip(variant_weights, original_prices, selling_prices,
                                                                      stocks, unit):
            if weight and original_price and selling_price and stock and unit:
                variant = ProductVariant()
                # product = Product.objects.get(product_name=product_name)
                variant.product = product
                variant.weight = Decimal(weight)

                if product.original_price == 0:
                    product.original_price = Decimal(original_price)
                if product.selling_price == 0:
                    product.selling_price = Decimal(selling_price)
                if product.stock == 0:
                    product.stock = stock

                variant.original_price = Decimal(original_price)
                variant.selling_price = Decimal(selling_price)
                variant.stock = stock
                variant.unit = unit
                product.save()
                variant.save()
                for img in images:
                    ProductImage.objects.create(product=product, image=img)

        return redirect('view_products')
        product.save()

    return render(request, 'adminside/product/view_products.html')


def Product_Unlist(request, product_id):
    product = Product.objects.get(id=product_id)
    sub_cat = Sub_Category.objects.filter(is_visible=True).order_by('id')
    if product.is_visible:
        product.is_visible = False
        product.save()
        product = Product.objects.all().order_by('id')
        context = {
            'products': product,
            'sub_cat': sub_cat
        }
        return render(request, 'adminside/product/view_products.html', context)
    else:
        product.is_visible = True
        product.save()
        product = Product.objects.all().order_by('id')
        context = {
            'products': product,
            'sub_cat': sub_cat
        }
        return render(request, 'adminside/product/view_products.html', context)


def Edit_Product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        product.product_name = request.POST.get('product_name')
        product.description = request.POST.get('description')
        sub_category = request.POST.get('category_name')
        sub_cat = Sub_Category.objects.get(id=sub_category)
        product.sub_category = sub_cat
        product.category = sub_cat.category
        # product.original_price = request.POST.get('original_price')
        # product.selling_prince = request.POST.get('selling_price')
        img1 = request.FILES.get('img')
        if img1 is None:
            product.images = product.images
        else:
            product.images = request.FILES.get('img')
        # product.stock = request.POST.get('stock')
        product.save()

        variant_weights = request.POST.getlist("variant_weight[]")
        original_prices = request.POST.getlist("variant_original_price[]")
        selling_prices = request.POST.getlist("variant_selling_price[]")
        stocks = request.POST.getlist('variant_stock[]')

        for weight, original_price, selling_price, stock in zip(variant_weights, original_prices, selling_prices,
                                                                stocks):
            if weight and original_price and selling_price and stock:
                variant = ProductVariant()
                variant.product = product
                variant.weight = Decimal(weight)
                variant.original_price = Decimal(original_prices)
                variant.selling_price = Decimal(selling_prices)
                variant.stock = stocks
                variant.save()

        return redirect('view_products')
    return redirect('view_products')


def ViewVariant(request, variant_id):
    product = Product.objects.get(id=variant_id)
    variants = ProductVariant.objects.filter(product=product).order_by('id')
    context = {
        'variants': variants,
    }

    return render(request, 'adminside/product/view_variant.html', context)


def SingleProductView(request, product_id):
    selected_product = ProductVariant.objects.get(id=product_id)
    product = Product.objects.get(id=selected_product.product.id)
    product_variant = ProductVariant.objects.filter(product=product)
    cart_id = _cart_id(request)
    in_cart = CartItem.objects.filter(cart__cart_id=cart_id, product=product).exists()
    images = ProductImage.objects.filter(product=product)
    similar_product = ProductVariant.objects.filter(product__category=product.category)[:4]

    try:
        orderproduct = OrderItem.objects.filter(user=request.user,product = product).exists()
    except OrderItem.DoesNotExist:
        orderproduct = None

    # get the review
    reviews = ReviewRating.objects.filter(product=product, status =True)
    context = {
        'product': selected_product,
        'variants': product_variant,
        'in_cart': in_cart,
        'images': images,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'similar_product': similar_product,
    }
    return render(request, 'user/single_product_view/single_product_view.html', context)


def single_product_weight_ajax(request, selected_value):
    # Your logic here, use the 'selected_value' parameter as needed
    variant = ProductVariant.objects.get(id=selected_value)
    selling_price = variant.selling_price
    weight = variant.weight
    stock = variant.stock
    original_price = variant.original_price
    if stock > 0:
        stock = "In Stock"
    else:
        stock = "Out Of Stock"

    data = {"selling_price": f"{selling_price}",
            "stock": f"{stock}",
            "weight": f"{weight} {variant.unit}",
            "weightt": f"{variant.weight}",
            "original_price": f"{original_price}"
            }
    return JsonResponse(data)


def edit_variant(request, variant_id):
    variant = ProductVariant.objects.get(id=variant_id)
    if request.method == 'POST':
        variant.weight = request.POST.get('variant_weight')
        variant.original_price = request.POST.get('variant_original_price')
        variant.selling_price = request.POST.get('variant_selling_price')
        variant.stock = request.POST.get('variant_stock')
        variant.save()
        variants = ProductVariant.objects.filter(product=variant.product).order_by('id')

        context = {
            'variants': variants,
        }
        return render(request, 'adminside/product/view_variant.html', context)
    return render(request, 'adminside/product/view_variant.html')


def variant_unlist(request, variant_id):
    variant = ProductVariant.objects.get(id=variant_id)
    if variant.is_available:
        variant.is_available = False
        variant.save()
        variants = ProductVariant.objects.filter(product=variant.product).order_by('id')
        context = {
            'variants': variants,
        }
        return render(request, 'adminside/product/view_variant.html', context)
    else:
        variant.is_available = True
        variant.save()
        variants = ProductVariant.objects.filter(product=variant.product).order_by('id')
        context = {
            'variants': variants,
        }
        return render(request, 'adminside/product/view_variant.html', context)


def view_images(request, product_id):
    images = ProductImage.objects.filter(product=product_id)
    product = Product.objects.get(id=product_id)
    context = {
        'images': images,
        'product': product,
    }
    return render(request, 'adminside/product/view_images.html', context)


def add_product_images(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        images = request.FILES.getlist('img')
        print(product.product_name, images)
        if images:
            for image in images:
                # Create a ProductImage instance for each image
                p = ProductImage(product=product, image=image)
                # Save the instance
                p.save()

    images = ProductImage.objects.filter(product=product_id)
    context = {
        'images': images,
        'product': product,
    }
    return redirect(reverse('view_images', args=[product.id]))


def delete_product_images(request, image_id):
    image = ProductImage.objects.get(id=image_id)
    product = Product.objects.get(id=image.product.id)
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, str(image.image))
        image.delete()
        if os.path.exists(file_path):
            os.remove(file_path)
    except:
        pass
    images = ProductImage.objects.filter(product=product)
    context = {
        'images': images,
        'product': product,
    }
    return redirect(reverse('view_images', args=[product.id]))


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=product_id)
    print(product)
    user =CustomUser.objects.get(email=request.user.email)
    print(user)
    if request.method == 'POST':

        try:
            reviews = ReviewRating.objects.get(user=user, product=product)
            # updating review
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, "Thanks you! Your review has been updated.")
            return redirect(url)
        except ReviewRating.DoesNotExist:
            # create a new review
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product = product
                data.user = user
                data.save()
                messages.success(request, "Thanks you! Your review has been submitted.")
                return redirect(url)
