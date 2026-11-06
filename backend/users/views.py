from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import User
from .serializers import (
    UserSerializer,
    UserMeSerializer,
    CustomTokenObtainPairSerializer,
    RegisterSerializer,
)


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary="Listar usuarios",
    operation_description="Obtiene el listado de todos los usuarios registrados en el sistema escolar. Requiere permisos de administrador (is_staff=True).",
    tags=['Administración de Usuarios']
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary="Crear nuevo usuario",
    operation_description="Registra un nuevo usuario en CampusConnect. La contraseña se cifra de forma segura usando PBKDF2/SHA256 y nunca se expone en la respuesta. Requiere permisos de administrador.",
    tags=['Administración de Usuarios']
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary="Consultar usuario por ID",
    operation_description="Obtiene los datos de un usuario específico a partir de su ID. Requiere permisos de administrador.",
    tags=['Administración de Usuarios']
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary="Actualizar usuario completamente (PUT)",
    operation_description="Actualiza todos los campos de un usuario. Si no se envía 'password', la contraseña del usuario se mantiene intacta. Si se envía una nueva contraseña, se cifra debidamente.",
    tags=['Administración de Usuarios']
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary="Actualizar usuario parcialmente (PATCH)",
    operation_description="Actualiza uno o varios campos de un usuario (por ejemplo, nombre o matrícula). Si no se envía el campo 'password', su contraseña actual NO cambia ni se ve alterada por la cuenta del administrador (corrección del error de seguridad del manual).",
    tags=['Administración de Usuarios']
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary="Eliminar usuario",
    operation_description="Elimina permanentemente a un usuario del sistema escolar. Requiere permisos de administrador.",
    tags=['Administración de Usuarios']
))
class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para la administración completa de usuarios (CRUD).
    Solo accesible para usuarios administradores (is_staff=True).
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserMeView(APIView):
    """
    Endpoint para consultar los datos personales del usuario que ha iniciado sesión.
    Requiere autenticación mediante token JWT (Bearer Token).
    Obtiene la información directamente desde request.user de manera segura.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id="auth_me_read",
        operation_summary="Consultar datos del usuario autenticado (/auth/me/)",
        operation_description=(
            "Devuelve la información del usuario que inició sesión basada en el token JWT. "
            "No permite consultar los datos de otros usuarios alterando parámetros y "
            "nunca devuelve contraseñas ni sus hashes."
        ),
        responses={
            200: UserMeSerializer,
            401: openapi.Response(
                description="No autenticado",
                examples={"application/json": {"detail": "Las credenciales de autenticación no se proveyeron."}}
            ),
        },
        tags=['Autenticación y Perfil']
    )
    def get(self, request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Endpoint para iniciar sesión con correo electrónico y contraseña.
    Devuelve un par de tokens JWT: access token (30 min) y refresh token (1 día).
    """
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        operation_summary="Iniciar sesión y obtener tokens JWT (/auth/token/)",
        operation_description=(
            "Recibe el email y la contraseña del usuario. "
            "Si las credenciales son válidas, devuelve el 'access' token (duración 30 minutos) "
            "y el 'refresh' token (duración 1 día)."
        ),
        tags=['Autenticación y Perfil']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RegisterView(APIView):
    """
    Endpoint público para registrar nuevos usuarios desde el frontend de React.
    No requiere autenticación previa.

    CORRECCIONES DE SEGURIDAD respecto al manual:
    - Los datos se leen del cuerpo de la petición (request.data), no del request.user.
    - El registro nunca otorga permisos de administrador.
    - La contraseña se cifra con set_password() y NO se devuelve en la respuesta.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Registrar nuevo usuario (público) (/auth/register/)",
        operation_description=(
            "Permite a cualquier visitante crear una cuenta en CampusConnect. "
            "No requiere autenticación. Los datos ingresados pertenecen al nuevo usuario, "
            "nunca al solicitante. Los permisos de administrador nunca se otorgan por este endpoint."
        ),
        request_body=RegisterSerializer,
        responses={
            201: RegisterSerializer,
            400: openapi.Response(
                description="Datos inválidos o email ya registrado",
                examples={"application/json": {"email": ["Ya existe un usuario con este correo electrónico."]}}
            ),
        },
        tags=['Autenticación y Perfil']
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'message': '¡Registro exitoso! Ya puedes iniciar sesión en CampusConnect.',
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'matricula': user.matricula,
                    }
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
