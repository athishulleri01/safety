from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from product.models import Product, ProductVariant
from .models import Category, Sub_Category


# Create your views here.
# <------------------------------------------------------Start Category------------------------------------------------------>

# <----------------------Add Category------------------------->
def AddCategory(request):
    if request.method == 'POST':
        cat = Category()
        category_name = request.POST.get('category_name')
        cat.category_name =category_name
        cat.slug=category_name.replace(" ", "-")
        cat.description = request.POST.get('description')
        cat.cat_image = request.FILES.get('cat_img')
        cat.save()
        return redirect('view_category')


# <----------------------Add Category------------------------->


# <----------------------View Category------------------------->
def ViewCategory(request):
    category = Category.objects.all().order_by('id')
    paginator = Paginator(category, 3)
    page_number = request.GET.get('page', 1)
    category = paginator.get_page(page_number)
    context = {
        'categories': category
    }
    return render(request, 'adminside/category/view_category.html', context)


# <----------------------View Category------------------------->


# <--------------List and unlist Category---------------------->

def Unlist(request, cat_id):
    cat = Category.objects.get(id=cat_id)
    if cat.is_visible:
        cat.is_visible = False
        cat.save()

        try:
            sub=Sub_Category.objects.filter(category=cat)
            for item in sub:
                item.is_visible = False
                item.save()
                try:
                    products =Product.objects.filter(category = cat)
                    for product in products:
                        product.is_visible = False
                        product.save()
                        try:
                            variants = ProductVariant.objects.filter(product=product)
                            for variant in variants:
                                variant.is_available = False
                                variant.save()
                        except:
                            pass
                except:
                    pass
        except:
            pass
        cat = Category.objects.all().order_by('id')
        context = {
            'categories': cat
        }
        return render(request, 'adminside/category/view_category.html', context)
    else:
        cat.is_visible = True
        cat.save()

        try:
            sub=Sub_Category.objects.filter(category=cat)
            for item in sub:
                item.is_visible = True
                item.save()
                try:
                    products =Product.objects.filter(category = cat)
                    for product in products:
                        product.is_visible = True
                        product.save()
                        try:
                            variants = ProductVariant.objects.filter(product=product)
                            for variant in variants:
                                variant.is_available = True
                                variant.save()
                        except:
                            pass
                except:
                    pass
        except:
            pass
        cat = Category.objects.all().order_by('id')
        context = {
            'categories': cat
        }
        return render(request, 'adminside/category/view_category.html', context)


# <--------------List and unlist Category---------------------->

# <---------------------Edit Category-------------------------->
def Edit_category(request, category_id):
    cat = Category.objects.get(id=category_id)
    if request.method == 'POST':
        cat.category_name = request.POST.get('category_name')
        cat.description = request.POST.get('description')
        img = request.FILES.get('cat_img')
        if img is None:
            cat.cat_image = cat.cat_image
        else:
            cat.cat_image = request.FILES.get('cat_img')
        cat.save()
        cat = Category.objects.all().order_by('id')
        context = {
            'categories': cat
        }
        return redirect('view_category')


# <---------------------Edit Category-------------------------->

# <----------------------------------------------------End Category------------------------------------------------------>


# <---------------------------------------------------Start Sub-Category------------------------------------------------->


# <-------------------Add Sub-Category-------------------------->
def AddSubCategory(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_name')
        category_instance = Category.objects.get(pk=category_id)
        sub_category_name = request.POST.get('sub_category_name')
        slug = sub_category_name.replace(" ", "-")
        description = request.POST.get('description')
        cat_image = request.FILES.get('cat_img')
        cat = Sub_Category(category=category_instance, sub_category_name=sub_category_name, description=description,
                           cat_image=cat_image, is_visible=True,slug=slug)
        cat.save()
        return redirect('view_subcategory')
    return render(request, 'adminside/sub_category/view_subcategory.html')


# <-------------------Add Sub-Category-------------------------->


# <-------------------View Sub-Category-------------------------->
def ViewSubCategory(request):
    cat = Category.objects.filter(is_visible=True)
    sub_cat = Sub_Category.objects.all().order_by('id')
    paginator = Paginator(sub_cat, 3)
    page_number = request.GET.get('page', 1)
    sub_cat = paginator.get_page(page_number)
    context = {
        'categories': cat,
        'sub_cat': sub_cat
    }
    return render(request, 'adminside/sub_category/view_subcategory.html', context)


# <-------------------View Sub-Category-------------------------->

# <---------------List and Unlist Sub-Category------------------->
def sub_Unlist(request, subcat_id):
    cat = Sub_Category.objects.get(id=subcat_id)

    if cat.is_visible:
        cat.is_visible = False
        cat.save()
        try:
            products = Product.objects.filter(sub_category=cat)
            for product in products:
                product.is_visible = False
                product.save()
                try:
                    variants = ProductVariant.objects.filter(product=product)
                    for variant in variants:
                        variant.is_available = False
                        variant.save()
                except:
                    pass
        except:
            pass
        cat = Sub_Category.objects.all().order_by('id')
        context = {
            'sub_cat': cat,
            # 'category': cat
        }
        return render(request, 'adminside/sub_category/view_subcategory.html', context)
    else:
        cat.is_visible = True
        cat.save()
        try:
            products = Product.objects.filter(sub_category=cat)
            for product in products:
                product.is_visible = True
                product.save()
                try:
                    variants = ProductVariant.objects.filter(product=product)
                    for variant in variants:
                        variant.is_available = True
                        variant.save()
                except:
                    pass
        except:
            pass
        cat = Sub_Category.objects.all().order_by('id')
        context = {
            'sub_cat': cat
        }
        return render(request, 'adminside/sub_category/view_subcategory.html', context)


# <---------------List and Unlist Sub-Category------------------->

# <---------------------Edit Sub-Category------------------------>
def Edit_Subcategory(request, subcat_id):
    cat = Sub_Category.objects.get(id=subcat_id)
    if request.method == 'POST':
        category_id = request.POST.get('category_name')
        cat.category = Category.objects.get(pk=category_id)
        cat.sub_category_name = request.POST.get('sub_category_name')
        cat.description = request.POST.get('description')
        img = request.FILES.get('cat_img')
        if img is None:
            cat.cat_image = cat.cat_image
        else:
            cat.cat_image = request.FILES.get('cat_img')
        cat.is_visible = True
        cat.save()
        cat = Category.objects.filter(is_visible=True)
        sub_cat = Sub_Category.objects.all().order_by('id')
        context = {
            'categories': cat,
            'sub_cat': sub_cat
        }
        return render(request, 'adminside/sub_category/view_subcategory.html', context)


# <---------------------Edit Sub-Category------------------------>

# <---------------------------------------------------End Sub-Category------------------------------------------------->

def ShowCategoryProduct(request, cat_id):
    sub_cat = Sub_Category.objects.all()
    products_with_default_variants = Product.objects.filter(sub_category=cat_id).prefetch_related('variants')
    product_queryset = ProductVariant.objects.none()
    for product in products_with_default_variants:
        default_variant = product.variants.filter(is_available=True).first()
        if default_variant:
            product_queryset |= ProductVariant.objects.filter(pk=default_variant.pk)
    paginator = Paginator(product_queryset, 6)
    page_number = request.GET.get('page', 1)
    product_queryset = paginator.get_page(page_number)
    context={
        'cat_products': product_queryset,
        'sub_category': sub_cat,
    }
    return render(request, 'user/shop/shop.html',context)
