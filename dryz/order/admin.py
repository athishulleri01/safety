from django.contrib import admin

from order.models import Order,OrderItem,Coupon,Notification

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Coupon)
admin.site.register(Notification)
