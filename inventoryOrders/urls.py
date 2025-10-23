"""
URL configuration for inventoryOrders project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Мои контроллеры
from products.views import ProductViewSet
from users.views import RegisterView

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
#router.register(r'users', UserView, basename='auth')

urlpatterns = [
    # ссылка на админ панель
    path('admin/', admin.site.urls),

    # ссылка на сам API - продукты
    path('api/', include(router.urls)),

    # ссылки на токены и авторизацию
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/register/', RegisterView.as_view(), name='register'),

    # чтобы можно было авторизоваться в самом REST
    path('api-auth/', include('rest_framework.urls'))
]
