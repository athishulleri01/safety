from django.conf.global_settings import MEDIA_ROOT
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('home.urls')),
    path('', include('dashboard.urls')),
    path('', include('product.urls')),
    path('', include('order.urls')),
    path('', include('categories.urls')),
    path('cart/', include('carts.urls')),
    path('wishlist/', include('wishlist.urls')),
    ]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

handler404 = 'home.views.error_404_view'
