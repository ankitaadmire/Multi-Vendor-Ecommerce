from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('adminpanel/', include('adminpanel.urls')),
    path('cart/', include('cart.urls')),
    path("orders/", include("orders.urls")),
    path("reviews/", include("reviews.urls")),
    path("wishlist/", include("wishlist.urls")),
    path('checkout/', include('checkout.urls')),
    path('notifications/', include('notifications.urls')),
    path("api/", include("api.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair",),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh",),
    path("chat/", include("chat.urls")),
    path("notifications/", include("notifications.urls")),
         

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

