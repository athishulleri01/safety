from django.db import models

from accounts.models import CustomUser
from product.models import ProductVariant


# Create your models here.
class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser,  on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

