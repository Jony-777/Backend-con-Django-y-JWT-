from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class CampusConnectSecurityAndAPITests(APITestCase):
    """
    Suite de pruebas obligatorias para CampusConnect:
    - Prueba 1: Creación de usuario y cifrado de contraseña.
    - Prueba 2: Login con email y obtención de tokens JWT (access y refresh).
    - Prueba 3: Consulta de datos personales (/auth/me/) sin exponer contraseñas/hashes.
    - Prueba 4: Actualización sin contraseña (corrección del error del manual).
    - Prueba 5: Actualización con nueva contraseña.
    - Prueba 6: Seguridad general (ninguna respuesta expone contraseñas ni hashes).
    - Prueba 7: Permisos (usuarios no autenticados bloqueados, solo admin en CRUD).
    """

    def setUp(self):
        # Superusuario / Administrador para operaciones del CRUD
        self.admin_email = "admin@campusconnect.edu"
        self.admin_password = "AdminPassword123!"
        self.admin_user = User.objects.create_superuser(
            email=self.admin_email,
            password=self.admin_password,
            first_name="Admin",
            last_name="Principal",
        )

        # Usuario alumno regular
        self.student_email = "alumno@campusconnect.edu"
        self.student_password = "AlumnoPassword2026!"
        self.student_user = User.objects.create_user(
            email=self.student_email,
            password=self.student_password,
            first_name="Carlos",
            last_name="Ramírez",
            matricula="MAT-2026-001",
        )

        # URLs
        self.token_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')
        self.register_url = reverse('user_register')
        self.me_url = reverse('user_me')
        self.users_list_url = reverse('user-list')

    # =========================================================================
    # PRUEBA 1. Creación de usuario
    # =========================================================================
    def test_01_user_creation_and_password_hashing(self):
        """
        Verifica que al crear un usuario:
        - Se almacena con email, first_name, last_name, matricula.
        - La contraseña se almacena CIFRADA (set_password), nunca en texto plano.
        - La respuesta HTTP 201 no expone el campo password ni hashes.
        """
        self.client.force_authenticate(user=self.admin_user)
        payload = {
            "email": "nuevo.estudiante@campusconnect.edu",
            "password": "PasswordSegura789!",
            "first_name": "Ana",
            "last_name": "Gómez",
            "matricula": "MAT-2026-002",
        }

        response = self.client.post(self.users_list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verificar que el campo password no se devuelve en la respuesta
        self.assertNotIn("password", response.data)
        self.assertEqual(response.data["email"], payload["email"])
        self.assertEqual(response.data["matricula"], payload["matricula"])

        # Verificar en la base de datos
        created_user = User.objects.get(email=payload["email"])
        self.assertEqual(created_user.first_name, "Ana")
        self.assertEqual(created_user.last_name, "Gómez")
        self.assertEqual(created_user.matricula, "MAT-2026-002")

        # La contraseña NO debe ser el texto plano
        self.assertNotEqual(created_user.password, payload["password"])
        # Debe ser un hash válido de Django (inicia con algoritmo como pbkdf2_sha256$)
        self.assertTrue(created_user.password.startswith("pbkdf2_sha256$"))
        # Debe validar correctamente con check_password
        self.assertTrue(created_user.check_password(payload["password"]))

    # =========================================================================
    # PRUEBA 2. Login con JWT
    # =========================================================================
    def test_02_login_jwt_token_obtain(self):
        """
        Verifica que un usuario pueda iniciar sesión con email y contraseña,
        obteniendo los tokens 'access' y 'refresh'.
        """
        payload = {
            "email": self.student_email,
            "password": self.student_password,
        }
        response = self.client.post(self.token_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertTrue(len(response.data["access"]) > 20)
        self.assertTrue(len(response.data["refresh"]) > 20)

    # =========================================================================
    # PRUEBA 3. Datos personales (/api/v1/auth/me/)
    # =========================================================================
    def test_03_auth_me_endpoint(self):
        """
        Verifica que al consultar /auth/me/ con token:
        - Devuelve id, email, first_name, last_name, matricula, is_active.
        - NO devuelve password, password_hash ni información sensible.
        - Obtiene al usuario de request.user sin permitir suplantar a otro por parámetro.
        """
        # Obtenemos token
        login_res = self.client.post(self.token_url, {
            "email": self.student_email,
            "password": self.student_password
        }, format='json')
        access_token = login_res.data["access"]

        # Consultamos /auth/me/ con Bearer Token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["id"], self.student_user.id)
        self.assertEqual(data["email"], self.student_email)
        self.assertEqual(data["first_name"], self.student_user.first_name)
        self.assertEqual(data["last_name"], self.student_user.last_name)
        self.assertEqual(data["matricula"], self.student_user.matricula)
        self.assertEqual(data["is_active"], True)

        # Comprobación de seguridad: NO expone contraseñas ni hashes
        self.assertNotIn("password", data)
        self.assertNotIn("password_hash", data)

        # Intentar pasar otro id por parámetro query no debe cambiar el usuario devuelto
        response_tampered = self.client.get(f"{self.me_url}?id={self.admin_user.id}")
        self.assertEqual(response_tampered.data["id"], self.student_user.id)

    # =========================================================================
    # PRUEBA 4. Actualización sin contraseña (CORRECCIÓN CRÍTICA DEL MANUAL)
    # =========================================================================
    def test_04_update_without_password_preserves_original_password(self):
        """
        PRUEBA OBLIGATORIA:
        1. Crear usuario con contraseña conocida.
        2. Comprobar que inicia sesión.
        3. Administrador actualiza nombre/apellido/matrícula SIN enviar password.
        4. Volver a iniciar sesión con la contraseña original.
        5. Comprobar que sigue funcionando.
        6. Comprobar que la contraseña NO cambió ni se asignó la del administrador.
        """
        # 1. Crear usuario
        original_pass = "ClaveOriginal123!"
        target_user = User.objects.create_user(
            email="alumno.modificar@campusconnect.edu",
            password=original_pass,
            first_name="Luis",
            last_name="Pérez",
            matricula="MAT-2026-003",
        )
        original_hash = target_user.password

        # 2. Comprobar login exitoso inicial
        login_res1 = self.client.post(self.token_url, {
            "email": target_user.email,
            "password": original_pass
        }, format='json')
        self.assertEqual(login_res1.status_code, status.HTTP_200_OK)

        # 3. El administrador actualiza al usuario mediante PATCH sin enviar campo 'password'
        self.client.force_authenticate(user=self.admin_user)
        detail_url = reverse('user-detail', kwargs={'pk': target_user.id})

        patch_data = {
            "first_name": "Luis Alberto",
            "last_name": "Pérez Morales",
            "matricula": "MAT-2026-999"
        }
        patch_response = self.client.patch(detail_url, patch_data, format='json')
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertNotIn("password", patch_response.data)

        # 4 & 5. Volver a iniciar sesión con la contraseña original
        self.client.credentials()  # Limpiar credenciales
        login_res2 = self.client.post(self.token_url, {
            "email": target_user.email,
            "password": original_pass
        }, format='json')
        self.assertEqual(
            login_res2.status_code,
            status.HTTP_200_OK,
            "La contraseña original DEBE seguir funcionando tras una actualización sin enviar password."
        )

        # 6. Comprobar que la contraseña no cambió y NO se asignó la del admin
        target_user.refresh_from_db()
        self.assertEqual(target_user.first_name, "Luis Alberto")
        self.assertEqual(target_user.matricula, "MAT-2026-999")
        self.assertEqual(target_user.password, original_hash)
        self.assertNotEqual(target_user.password, self.admin_user.password)

        # Comprobar también con PUT
        self.client.force_authenticate(user=self.admin_user)
        put_data = {
            "email": target_user.email,
            "first_name": "Luis Alberto Modificado",
            "last_name": "Pérez",
            "matricula": "MAT-2026-999",
            "is_active": True,
            "is_staff": False,
        }
        put_response = self.client.put(detail_url, put_data, format='json')
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        self.client.credentials()
        login_res3 = self.client.post(self.token_url, {
            "email": target_user.email,
            "password": original_pass
        }, format='json')
        self.assertEqual(
            login_res3.status_code,
            status.HTTP_200_OK,
            "La contraseña original debe mantenerse también tras un PUT sin password."
        )

    # =========================================================================
    # PRUEBA 5. Actualización con contraseña
    # =========================================================================
    def test_05_update_with_password(self):
        """
        Verifica que al enviar una nueva contraseña en la actualización:
        - La contraseña anterior deja de funcionar.
        - La nueva contraseña permite iniciar sesión correctamente.
        - La contraseña se almacena cifrada.
        """
        target_user = User.objects.create_user(
            email="cambio.pass@campusconnect.edu",
            password="PasswordVieja123!",
            first_name="Elena",
            last_name="Torres",
            matricula="MAT-2026-004",
        )
        detail_url = reverse('user-detail', kwargs={'pk': target_user.id})

        # Administrador actualiza la contraseña
        self.client.force_authenticate(user=self.admin_user)
        new_password = "PasswordNueva456!"
        response = self.client.patch(detail_url, {"password": new_password}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("password", response.data)

        # Probar login con contraseña vieja (debe fallar 401)
        self.client.credentials()
        fail_login = self.client.post(self.token_url, {
            "email": target_user.email,
            "password": "PasswordVieja123!"
        }, format='json')
        self.assertEqual(fail_login.status_code, status.HTTP_401_UNAUTHORIZED)

        # Probar login con contraseña nueva (debe ser exitoso 200)
        success_login = self.client.post(self.token_url, {
            "email": target_user.email,
            "password": new_password
        }, format='json')
        self.assertEqual(success_login.status_code, status.HTTP_200_OK)
        self.assertIn("access", success_login.data)

    # =========================================================================
    # PRUEBA 6. Seguridad (sin exposición de contraseñas ni hashes)
    # =========================================================================
    def test_06_no_password_or_hash_exposed_in_any_response(self):
        """
        Verifica que ningún endpoint (GET list, GET detail, POST create, PUT, PATCH, auth/me)
        exponga 'password', 'password_hash' ni hashes en ninguna respuesta.
        """
        self.client.force_authenticate(user=self.admin_user)

        # GET lista
        res_list = self.client.get(self.users_list_url)
        self.assertEqual(res_list.status_code, status.HTTP_200_OK)
        for item in res_list.data:
            self.assertNotIn("password", item)
            self.assertNotIn("hash", item)

        # GET detalle
        detail_url = reverse('user-detail', kwargs={'pk': self.student_user.id})
        res_detail = self.client.get(detail_url)
        self.assertEqual(res_detail.status_code, status.HTTP_200_OK)
        self.assertNotIn("password", res_detail.data)

        # auth/me
        self.client.force_authenticate(user=self.student_user)
        res_me = self.client.get(self.me_url)
        self.assertEqual(res_me.status_code, status.HTTP_200_OK)
        self.assertNotIn("password", res_me.data)

    # =========================================================================
    # PRUEBA 7. Permisos
    # =========================================================================
    def test_07_permissions_unauthenticated_and_regular_users(self):
        """
        Verifica que:
        - Usuarios no autenticados NO pueden acceder a /auth/me/ (401).
        - Usuarios no autenticados NO pueden acceder al CRUD de /users/ (401).
        - Usuarios regulares (no admin) NO pueden acceder al CRUD de /users/ (403).
        - Solo administradores (is_staff=True) pueden acceder al CRUD de /users/.
        """
        self.client.credentials()  # Sin autenticación

        # Anónimo en /auth/me/ -> 401
        res1 = self.client.get(self.me_url)
        self.assertEqual(res1.status_code, status.HTTP_401_UNAUTHORIZED)

        # Anónimo en /users/ -> 401
        res2 = self.client.get(self.users_list_url)
        self.assertEqual(res2.status_code, status.HTTP_401_UNAUTHORIZED)

        # Usuario alumno (autenticado pero is_staff=False) en /users/ -> 403 Forbidden
        self.client.force_authenticate(user=self.student_user)
        res3 = self.client.get(self.users_list_url)
        self.assertEqual(res3.status_code, status.HTTP_403_FORBIDDEN)

        # Administrador (is_staff=True) en /users/ -> 200 OK
        self.client.force_authenticate(user=self.admin_user)
        res4 = self.client.get(self.users_list_url)
        self.assertEqual(res4.status_code, status.HTTP_200_OK)

    # =========================================================================
    # PRUEBA 8. Registro público de usuarios (/api/v1/auth/register/)
    # =========================================================================
    def test_08_public_user_registration(self):
        """
        Verifica que el registro público:
        - Funcione sin autenticación previa (AllowAny).
        - Cree el usuario con contraseña cifrada en Django.
        - No otorgue permisos de administrador (is_staff=False, is_superuser=False).
        - No exponga la contraseña en la respuesta.
        - Permita al nuevo usuario iniciar sesión inmediatamente con el endpoint /auth/token/.
        """
        self.client.credentials()  # Sin token ni credenciales
        payload = {
            "email": "estudiante.registrado@campusconnect.edu",
            "password": "PasswordRegistro2026!",
            "first_name": "Valeria",
            "last_name": "Sánchez",
            "matricula": "MAT-2026-REG",
        }
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", response.data)
        if "user" in response.data:
            self.assertNotIn("password", response.data["user"])

        # Verificar en base de datos
        new_user = User.objects.get(email=payload["email"])
        self.assertEqual(new_user.first_name, "Valeria")
        self.assertEqual(new_user.matricula, "MAT-2026-REG")
        self.assertFalse(new_user.is_staff)
        self.assertFalse(new_user.is_superuser)
        self.assertTrue(new_user.check_password(payload["password"]))

        # Verificar que el nuevo usuario puede iniciar sesión y obtener tokens
        login_res = self.client.post(self.token_url, {
            "email": payload["email"],
            "password": payload["password"]
        }, format='json')
        self.assertEqual(login_res.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_res.data)
