from django.urls import path
from . import views

urlpatterns = [
    path('wish_list', views.wishlist, name='wish_list'),
    path('add_wishlist/<int:variant_id>', views.add_whishlit, name='add_wishlist'),
    path('remove_wish_list/<int:wish_id>', views.remove_wish_list, name='remove_wish_list'),
    path('add_wish_to_cart/<int:wish_id>', views.add_wish_to_cart, name='add_wish_to_cart'),
]
