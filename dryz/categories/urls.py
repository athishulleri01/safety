from django.urls import path
from . import views

urlpatterns = [
    # admin side

    path('view_category/', views.ViewCategory, name='view_category'),
    path('add_category/', views.AddCategory, name='add_category'),
    path('un-list/<int:cat_id>/', views.Unlist, name="un_list"),
    path('edit_categories/<int:category_id>/', views.Edit_category, name="edit_categories"),
    path('view_subcategory/', views.ViewSubCategory, name='view_subcategory'),
    path('add_subcategory/', views.AddSubCategory, name='add_subcategory'),
    path('sub_unlist/<int:subcat_id>/', views.sub_Unlist, name="sub_unlist"),
    path('edit_subcategories/<int:subcat_id>/', views.Edit_Subcategory, name="edit_subcategories"),

    # user side
    path('show_category_product/<int:cat_id>/', views.ShowCategoryProduct, name="show_category_product"),

]
