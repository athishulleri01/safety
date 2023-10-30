import os
from datetime import datetime

from django.db import models
from django.db.models import Avg, Count

from accounts.models import CustomUser
from categories.models import Category, Sub_Category
from django.utils import timezone
from imagefield.fields import ImageField
from django.utils.text import slugify
import datetime
from django.urls import reverse


# def getFileName(request, filename):
#     now_time = datetime.datetime.now().strftime("%Y%m%d%H:%M:%s")
#     new_filename = "%s%s" % (now_time, filename)
#     return os.path.join('uploads/',filename)


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    images = models.ImageField(upload_to="images/products/",default=None)
    is_available = models.BooleanField(default=True)
    original_price = models.FloatField(default=0)
    selling_price = models.FloatField(default=0)
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    trending = models.BooleanField(default=False, help_text="0-default,1-Hidden")
    sub_category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    modified_data = models.DateField(auto_now=True)
    is_visible = models.BooleanField(default=True)

    # def get_url(self):
    #     return reverse('single_product',args=[self.category.slug,self.slug])
    def __str__(self):
        return self.product_name

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    weight = models.FloatField()
    unit = models.CharField(max_length=2)
    original_price = models.FloatField(default=0)
    selling_price = models.FloatField(default=0)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.product_name} - {self.weight} g"


class VariationManager(models.Manager):
    def weights(self):
        return super(VariationManager, self).filter()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Change related_name
    image = models.ImageField(upload_to='images/product_images/')

    class Coupon(models.Model):
        coupon_name = models.CharField(max_length=100)
        coupon_code = models.CharField(max_length=100)
        min_price = models.IntegerField()
        coupon_discount_amount = models.PositiveIntegerField()
        start_date = models.DateField(default=timezone.now)
        end_date = models.DateField(default=timezone.now)
        is_available = models.BooleanField(default=True)

        def __str__(self):
            return self.coupon_name

        def is_coupon_expired(self):
            return timezone.now().date() >= self.end_date

    def __str__(self):
        return f"Image for {self.product.product_name}"



class ReviewRating(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    subject = models.CharField(max_length=100,blank=True)
    review = models.TextField(max_length=500,blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20,blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
