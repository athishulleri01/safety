from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/', views.remove, name='remove_cart'),
    path('increment_cart/<int:product_id>/', views.adding,
         name='increment_cart'),
    path('remove_cart_item/<int:product_id>/', views.remove_cart_item,
         name='remove_cart_item'),
    path('profile/', views.profile, name='profile'),
    path('address/', views.address, name='address'),
    path('add_address/', views.add_address, name='add_address'),
    path('add_address_checkout/', views.add_address_checkout,
         name='add_address_checkout'),
    path('edit_address/<int:address_id>', views.edit_address,
         name='edit_address'),
    path('delete_address/<int:address_id>', views.delete_address,
         name='delete_address'),
    path('checkout/', views.checkout, name='checkout'),
    path('my-order/<str:id>/', views.order, name='my_order'),
    path('my-order/', views.order, name='my_order'),
    path('selected_address/', views.selectedAddress, name='selected_address'),
    path('pdf-download/<int:id>', views.pdf_download, name='pdf_download'),

]
