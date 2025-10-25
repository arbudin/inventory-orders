from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from rest_framework import routers, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Мои контроллеры
from products.views import ProductViewSet
from users.views import RegisterView
from orders.views import CartViewSet,CheckoutViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'cart', CartViewSet, basename='cart')

# Схема для Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Inventory Orders API",
        default_version='v1',
        description="Документация для API управления продуктами, корзиной и заказами",
        contact=openapi.Contact(email="support@example.com"),
    ),
    public=True,
    permission_classes = (permissions.AllowAny,),
)

urlpatterns = [
    # ссылка на админ панель
    path('admin/', admin.site.urls),

    # ссылка на сам API - продукты
    path('api/', include(router.urls)),

    # ссылки на токены и авторизацию
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/register/', RegisterView.as_view(), name='register'),

    # чтобы можно было авторизоваться в самом REST
    path('api-auth/', include('rest_framework.urls')),

    # ссылки для корзины
    path('api/', include(router.urls)),

    # ссылки для checkout
    path('api/orders/checkout/', CheckoutViewSet.as_view(), name='checkout'),

    # Ссылки для Swagger и ReDoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),
]
