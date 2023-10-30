from django.db import models
import os
from django.utils import timezone


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    description = models.TextField(max_length=225, blank=True)
    is_visible = models.BooleanField(default=True)
    cat_image = models.ImageField(upload_to='images/category', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name


# def upload_to(instance, filename):
#     now = timezone.now()
#     base, ext = os.path.splitext(filename)
#     unique_filename = f"{now:%Y%m%d%H%M%S}{ext}"
#     return os.path.join("categories/", unique_filename)


class Sub_Category(models.Model):
    sub_category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200,unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(max_length=225,blank=False)
    cat_image = models.ImageField(upload_to='images/sub_category', blank=True)
    is_visible = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'sub category'
        verbose_name_plural = 'sub categories'

    def __str__(self):
        return self.sub_category_name
