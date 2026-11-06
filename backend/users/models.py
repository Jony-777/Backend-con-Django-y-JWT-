from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
    Administrador personalizado para el modelo User.
    Permite crear usuarios y superusuarios utilizando el correo electrónico
    como identificador único en lugar del username tradicional.
    """
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """
        Crea y guarda un usuario común con el email y contraseña dados.
        """
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crea y guarda un superusuario con permisos administrativos.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Modelo de usuario personalizado para la plataforma CampusConnect.
    Hereda de AbstractUser, sustituye el username por email y agrega el campo matrícula.
    """
    username = None  # Deshabilitamos el campo username por completo
    email = models.EmailField('Correo electrónico', unique=True)
    matricula = models.CharField('Matrícula', max_length=50, blank=True, default='')

    # Configuración de identificación y campos requeridos para createsuperuser
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['id']

    def __str__(self):
        if self.matricula:
            return f"{self.email} ({self.matricula})"
        return self.email
