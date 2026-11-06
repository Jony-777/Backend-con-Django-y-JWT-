from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para el CRUD de usuarios administrativos.
    Garantiza que la contraseña sea siempre write_only y gestiona
    su cifrado de forma segura tanto en la creación como en la actualización.
    """
    password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'},
        help_text='Contraseña del usuario. Se almacenará de forma cifrada mediante PBKDF2/SHA256.'
    )

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'matricula',
            'password',
            'is_active',
            'is_staff',
        ]
        read_only_fields = ['id']

    def validate(self, attrs):
        # Al crear un usuario (POST), la contraseña es obligatoria
        if self.instance is None and not attrs.get('password'):
            raise serializers.ValidationError({
                'password': 'La contraseña es obligatoria al registrar un nuevo usuario.'
            })
        return attrs

    def validate_password(self, value):
        if value is not None and len(value.strip()) < 6:
            raise serializers.ValidationError('La contraseña debe tener al menos 6 caracteres.')
        return value

    def create(self, validated_data):
        """
        Creación segura de usuario.
        Extrae la contraseña y la cifra con set_password().
        Nunca se almacena en texto plano ni se devuelve en la respuesta.
        """
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Actualización segura de usuario (PUT y PATCH).
        CORRECCIÓN DE SEGURIDAD DEL MANUAL:
        1. Si NO se envía 'password', la contraseña del usuario permanece INTACTA.
           Bajo ninguna circunstancia se asigna la contraseña del administrador solicitante.
        2. Si se envía una nueva 'password', se cifra mediante set_password().
        3. La contraseña nunca se expone en la respuesta ya que es write_only.
        """
        password = validated_data.pop('password', None)

        # Actualiza el resto de campos proporcionados
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Si se envió una nueva contraseña, se cifra y actualiza
        if password:
            instance.set_password(password)

        instance.save()
        return instance


class UserMeSerializer(serializers.ModelSerializer):
    """
    Serializer para el endpoint /api/v1/auth/me/.
    Devuelve exclusivamente información personal no sensible del usuario autenticado.
    No expone contraseñas, hashes ni campos confidenciales.
    """
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'matricula',
            'is_active',
        ]
        read_only_fields = fields


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer público para registrar nuevos usuarios desde el frontend.
    CORRECCIONES DE SEGURIDAD respecto al manual:
    - Los datos se obtienen del cuerpo de la petición (request.data), NO del usuario solicitante.
    - El registro público NUNCA otorga permisos de administrador (is_staff=False por defecto).
    - La contraseña se cifra con set_password() y nunca se devuelve en la respuesta.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=6,
        style={'input_type': 'password'},
        help_text='Contraseña del nuevo usuario (mínimo 6 caracteres).'
    )

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'matricula',
            'password',
        ]
        read_only_fields = ['id']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Ya existe un usuario con este correo electrónico.')
        return value

    def create(self, validated_data):
        """
        Crea un usuario nuevo con contraseña cifrada.
        El registro público siempre crea usuarios regulares (is_staff=False, is_superuser=False).
        Los datos vienen del formulario de registro, nunca del usuario solicitante.
        """
        password = validated_data.pop('password')
        user = User(
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            matricula=validated_data.get('matricula', ''),
            is_staff=False,        # El registro público nunca otorga permisos de admin
            is_superuser=False,
            is_active=True,
        )
        user.set_password(password)   # Cifrado seguro PBKDF2/SHA256
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer para el login JWT con email y password.
    Incluye datos adicionales del usuario dentro de los claims del token.
    """
    username_field = 'email'

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Claims personalizados en el token de acceso
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['matricula'] = user.matricula
        token['is_staff'] = user.is_staff
        return token

