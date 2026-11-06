from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Formulario para la creación de usuarios en el Django Admin
    adaptado al modelo personalizado con email.
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'matricula')


class CustomUserChangeForm(UserChangeForm):
    """
    Formulario para la edición de usuarios en el Django Admin.
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'matricula', 'is_active', 'is_staff', 'is_superuser')

