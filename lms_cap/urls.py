from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API Versioning
    path('api/v1/auth/', include('accounts.urls')),
    path('api/v1/customers/', include('customers.urls')),
    path('api/v1/products/', include('products.urls')),

    # JWT Refresh
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Swagger
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]