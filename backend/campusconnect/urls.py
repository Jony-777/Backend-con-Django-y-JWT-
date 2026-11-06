"""
URL configuration for campusconnect project.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuración del esquema de Swagger / OpenAPI
schema_view = get_schema_view(
    openapi.Info(
        title="CampusConnect API",
        default_version='v1',
        description=(
            "API RESTful para la administración de usuarios de la plataforma escolar CampusConnect.\n\n"
            "Incluye autenticación mediante JWT (JSON Web Tokens), endpoint de consulta de perfil (/auth/me/) "
            "y CRUD administrativo completo para usuarios escolares (/users/).\n\n"
            "Para autenticar peticiones en Swagger, haz clic en el botón 'Authorize' y usa: Bearer <tu_token_access>"
        ),
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="soporte@campusconnect.edu"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),

    # Rutas principales de la API v1
    path('api/v1/', include('users.urls')),

    # Documentación Swagger y ReDoc
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
