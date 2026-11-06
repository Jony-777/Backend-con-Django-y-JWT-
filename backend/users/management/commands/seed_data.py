from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Crea usuarios de prueba iniciales para CampusConnect (administrador y alumnos)'

    def handle(self, *args, **options):
        # 1. Crear Superusuario / Administrador
        admin_email = 'admin@campusconnect.edu'
        admin_pass = 'Admin123456!'
        if not User.objects.filter(email=admin_email).exists():
            admin = User.objects.create_superuser(
                email=admin_email,
                password=admin_pass,
                first_name='Admin',
                last_name='CampusConnect',
                matricula='ADM-001'
            )
            self.stdout.write(self.style.SUCCESS(
                f'Superusuario creado exitosamente:\n'
                f'  Email: {admin_email}\n'
                f'  Password: {admin_pass}\n'
                f'  Rol: Administrador (is_staff=True, is_superuser=True)'
            ))
        else:
            self.stdout.write(self.style.WARNING(f'El superusuario {admin_email} ya existe.'))

        # 2. Crear Alumno 1
        alumno1_email = 'carlos.ramirez@campusconnect.edu'
        alumno1_pass = 'Alumno123456!'
        if not User.objects.filter(email=alumno1_email).exists():
            User.objects.create_user(
                email=alumno1_email,
                password=alumno1_pass,
                first_name='Carlos',
                last_name='Ramírez',
                matricula='MAT-2026-001'
            )
            self.stdout.write(self.style.SUCCESS(
                f'Alumno 1 creado exitosamente:\n'
                f'  Email: {alumno1_email}\n'
                f'  Password: {alumno1_pass}\n'
                f'  Matrícula: MAT-2026-001'
            ))
        else:
            self.stdout.write(self.style.WARNING(f'El alumno {alumno1_email} ya existe.'))

        # 3. Crear Alumno 2
        alumno2_email = 'ana.torres@campusconnect.edu'
        alumno2_pass = 'Alumno123456!'
        if not User.objects.filter(email=alumno2_email).exists():
            User.objects.create_user(
                email=alumno2_email,
                password=alumno2_pass,
                first_name='Ana',
                last_name='Torres',
                matricula='MAT-2026-002'
            )
            self.stdout.write(self.style.SUCCESS(
                f'Alumno 2 creado exitosamente:\n'
                f'  Email: {alumno2_email}\n'
                f'  Password: {alumno2_pass}\n'
                f'  Matrícula: MAT-2026-002'
            ))
        else:
            self.stdout.write(self.style.WARNING(f'El alumno {alumno2_email} ya existe.'))

        self.stdout.write(self.style.SUCCESS('\n¡Datos de prueba listos para usar en Swagger y Django Admin!'))

