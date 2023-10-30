from django.urls import path
from . import views

urlpatterns = [
    # admin side
    path('view_products/', views.ViewProducts, name='view_products'),
    path('add_product/', views.AddProduct, name='add_product'),
    path('product_unlist/<int:product_id>/', views.Product_Unlist, name="product_unlist"),
    path('edit_product/<int:product_id>/', views.Edit_Product, name="edit_product"),
    path('view_variant/<int:variant_id>', views.ViewVariant, name="view_variant"),
    path('edit_variant/<int:variant_id>', views.edit_variant, name="edit_variant"),
    path('variant_unlist/<int:variant_id>/', views.variant_unlist, name="variant_unlist"),
    path('view_images/<int:product_id>/', views.view_images, name="view_images"),
    path('add_product_images/<int:product_id>/', views.add_product_images, name="add_product_images"),
    path('delete_product_images/<int:image_id>/', views.delete_product_images, name="delete_product_images"),

    # user side
    path('single_product/<int:product_id>', views.SingleProductView, name="single_product"),
    path('single_product_weight_ajax/<int:selected_value>/', views.single_product_weight_ajax,
         name='single_product_weight_ajax'),
    path('submit_review/<int:product_id>',views.submit_review, name="submit_review")



]
