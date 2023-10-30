
from django.urls import path
from . import views
urlpatterns = [
    path('home/', views.home, name='home'),
    path('view_shop/', views.ViewShop, name='view_shop'),
    # path('<slug:category_slug>', views.ViewShop, name='product_by_view'),
    path('search/',views.Search,name='search'),
    path('error_404_view/',views.error_404_view,name="error_404_view")

]

