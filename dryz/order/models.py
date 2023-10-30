from django.db import models

from accounts.models import CustomUser
from product.models import Product, ProductVariant
from carts.models import Address


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=250, null=True)
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=150, null=True)
    orderstatuses = (
        ('Order confirmed', 'Order confirmed'),
        ('Shipped', 'Shipped'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Return requested', 'Return requested'),
        ('Return processing', 'Return processing'),
        ('Returned', 'Returned'),
    )

    status = models.CharField(max_length=150, choices=orderstatuses, default='Order confirmed')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.tracking_no)


class OrderItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant=models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)
    STATUS = (
        ('Order confirmed', 'Order confirmed'),
        ('Shipped', 'Shipped'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Return requested', 'Return requested'),
        ('Return processing', 'Return processing'),
        ('Returned', 'Returned'),
    )
    status = models.CharField(max_length=150, choices=STATUS, default='Order Confirmed')

    def _str_(self):
        return f"{self.order.id, self.order.tracking_no}"


class ReturnOrder(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    order= models.ForeignKey(Order, on_delete=models.CASCADE)
    return_reason = models.CharField(max_length=100, null=True)
    return_comment = models.TextField(max_length=500, null=True)

    def __str__(self):
        return f"{self.id}"


class Coupon(models.Model):
    coupon_name=models.CharField(max_length=20)
    coupon_code=models.CharField(max_length=20)
    min_purchase = models.FloatField()
    coupon_discount = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.coupon_name


class Notification(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)