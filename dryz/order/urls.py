from django.urls import path
from . import views

urlpatterns = [
    path('view_coupons/', views.ViewCoupons, name='view_coupons'),
    path('add-coupon/', views.add_coupon, name='add_coupon'),
    path('delete_coupon/<int:id>/', views.delete_coupon, name='delete_coupon'),
    path('edit_coupon/<int:id>/', views.edit_coupon, name='edit_coupon'),
    path('proceed-to-pay/', views.razorpaycheck, name='proceed-to-pay'),
    path('wallet-payment/', views.wallet_payment, name='wallet-payment'),
    path('view_order_admin/', views.view_orders_admin, name='view_order_admin'),
    path('view_single_order_admin/<int:order_id>', views.view_single_order_admin, name='view_single_order_admin'),
    path('order_status/', views.order_status, name='order_status'),
    path('view_orders_user/', views.view_orders_user, name='view_orders_user'),
    path('track_order_status/<int:order_item_id>/', views.track_order_status, name='track_order_status'),
    path('cancel_order/<int:order_item_id>/', views.cancel_order, name='cancel_order'),
    path('return_order/<int:order_item_id>/', views.return_order, name='return_order'),
    path('return_approval/<int:order_id>/', views.return_approval, name='return_approval'),
    path('sales-report/', views.sales_report, name='sales_report'),
    path('sales-report-pdf/', views.sales_report_pdf_download, name='sales_report_pdf'),

]

