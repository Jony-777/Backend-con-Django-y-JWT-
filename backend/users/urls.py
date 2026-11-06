from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserViewSet,
    UserMeView,
    CustomTokenObtainPairView,
    RegisterView,
)

# Router para el CRUD de usuarios
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Autenticación JWT
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Registro público de nuevos usuarios (sin autenticación previa)
    path('auth/register/', RegisterView.as_view(), name='user_register'),

    # Datos del usuario autenticado
    path('auth/me/', UserMeView.as_view(), name='user_me'),

    # Rutas del CRUD administrativo de usuarios
    path('', include(router.urls)),
]
