from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Configuración personalizada del Django Admin para CampusConnect.
    Permite visualizar, crear y editar usuarios sin exponer contraseñas en texto plano ni hashes.
    """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    # Columnas mostradas en la lista del panel
    list_display = (
        'id',
        'email',
        'first_name',
        'last_name',
        'matricula',
        'is_active',
        'is_staff',
    )
    list_display_links = ('id', 'email')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name', 'matricula')
    ordering = ('id',)

    # Formulario para editar usuario existente
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Información personal'), {'fields': ('first_name', 'last_name', 'matricula')}),
        (
            _('Permisos y roles'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (_('Fechas'), {'fields': ('last_login', 'date_joined')}),
    )

    # Formulario para crear un nuevo usuario desde Django Admin
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'first_name',
                    'last_name',
                    'matricula',
                    'password1',
                    'password2',
                    'is_active',
                    'is_staff',
                ),
            },
        ),
    )
