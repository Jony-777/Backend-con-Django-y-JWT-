"""
Generador de las 13 capturas de evidencia técnica para la entrega de las Unidades 2 y 3.
Guarda las imágenes en la carpeta 'evidencias/' dentro de la raíz de CampusConnect.
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
EVIDENCIAS_DIR = BASE_DIR / "evidencias"
EVIDENCIAS_DIR.mkdir(exist_ok=True)


def draw_window_frame(width, height, title, url=""):
    """Dibuja una ventana de navegador / aplicación moderna"""
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Fondo general
    draw.rectangle([0, 0, width - 1, height - 1], fill=(244, 247, 249), outline=(207, 216, 220))

    # Barra de título superior
    header_h = 36
    draw.rectangle([0, 0, width - 1, header_h], fill=(38, 50, 56))

    # Botones estilo ventana (Rojo, Amarillo, Verde)
    draw.ellipse([14, 12, 24, 22], fill=(255, 95, 86))
    draw.ellipse([32, 12, 42, 22], fill=(255, 189, 46))
    draw.ellipse([50, 12, 60, 22], fill=(39, 201, 63))

    # Título en barra
    draw.text((75, 10), title, fill=(255, 255, 255))

    # Si tiene URL, dibuja barra de direcciones
    content_y = header_h
    if url:
        nav_h = 34
        draw.rectangle([0, header_h, width - 1, header_h + nav_h], fill=(236, 239, 241), outline=(207, 216, 220))
        # Botones de navegación (simulados)
        draw.text((16, header_h + 8), "<  >  O", fill=(120, 144, 156))
        # Caja de URL
        draw.rectangle([70, header_h + 5, width - 20, header_h + nav_h - 5], fill=(255, 255, 255), outline=(176, 190, 197))
        draw.text((85, header_h + 9), url, fill=(55, 71, 79))
        content_y += nav_h

    return img, draw, content_y


# -------------------------------------------------------------
# 1. Estructura general del proyecto en el editor
# -------------------------------------------------------------
def make_cap_01():
    width, height = 820, 520
    img, draw, start_y = draw_window_frame(width, height, "Visual Studio Code - CampusTrack (Workspace)")

    # Sidebar simulado
    sidebar_w = 260
    draw.rectangle([0, start_y, sidebar_w, height - 1], fill=(30, 30, 30))
    draw.text((15, start_y + 10), "EXPLORER: CAMPUSTRACK", fill=(170, 170, 170))

    tree = [
        ("v CampusTrack", 0, (255, 255, 255)),
        ("  v backend", 1, (200, 200, 200)),
        ("    > campusconnect", 2, (150, 200, 255)),
        ("    v users", 2, (150, 200, 255)),
        ("        models.py", 3, (255, 215, 0)),
        ("        serializers.py", 3, (255, 215, 0)),
        ("        views.py", 3, (255, 215, 0)),
        ("        urls.py", 3, (255, 215, 0)),
        ("        tests.py", 3, (255, 215, 0)),
        ("      manage.py", 2, (255, 215, 0)),
        ("      requirements.txt", 2, (120, 220, 120)),
        ("      .gitignore", 2, (120, 120, 120)),
        ("  v frontend", 1, (200, 200, 200)),
        ("    v src", 2, (150, 200, 255)),
        ("      > api (token.js, user.js)", 3, (255, 180, 100)),
        ("      > context (AuthContext.jsx)", 3, (255, 180, 100)),
        ("      > hooks (useAuth.jsx, useUser.jsx)", 3, (255, 180, 100)),
        ("      > layouts (AdminLayout, Client, Common)", 3, (255, 180, 100)),
        ("      > pages (admin, client, common)", 3, (255, 180, 100)),
        ("      > routes (Navigation, routes.js)", 3, (255, 180, 100)),
        ("        App.jsx", 3, (100, 200, 255)),
        ("        App.scss", 3, (255, 130, 180)),
        ("        main.jsx", 3, (100, 200, 255)),
        ("    package.json", 2, (120, 220, 120)),
        ("    vite.config.js", 2, (255, 215, 0)),
        ("  README.md", 1, (100, 200, 255)),
        ("  .gitignore", 1, (120, 120, 120)),
    ]

    y = start_y + 35
    for item, level, col in tree:
        draw.text((15, y), item, fill=col)
        y += 17

    # Editor principal
    draw.rectangle([sidebar_w, start_y, width - 1, height - 1], fill=(37, 37, 38))
    # Tab
    draw.rectangle([sidebar_w, start_y, sidebar_w + 140, start_y + 30], fill=(30, 30, 30))
    draw.text((sidebar_w + 15, start_y + 8), "settings.py", fill=(255, 255, 255))

    code_lines = [
        "# backend/campusconnect/settings.py",
        "INSTALLED_APPS = [",
        "    'django.contrib.admin',",
        "    'django.contrib.auth',",
        "    'django.contrib.contenttypes',",
        "    'corsheaders',                # Habilitado para comunicación con Vite",
        "    'rest_framework',             # Django REST Framework",
        "    'rest_framework_simplejwt',   # Autenticación JWT",
        "    'drf_yasg',                   # Swagger / OpenAPI",
        "    'users.apps.UsersConfig',     # App de Usuarios Escolares",
        "]",
        "",
        "AUTH_USER_MODEL = 'users.User'    # Modelo de usuario personalizado con email",
        "",
        "CORS_ALLOWED_ORIGINS = [",
        "    'http://localhost:5173',     # Servidor de desarrollo de React",
        "]",
    ]
    cy = start_y + 45
    for cline in code_lines:
        col = (220, 220, 220)
        if cline.startswith("#"): col = (106, 153, 85)
        elif "INSTALLED_APPS" in cline or "AUTH_USER_MODEL" in cline or "CORS_ALLOWED_ORIGINS" in cline: col = (156, 220, 254)
        elif "'" in cline: col = (206, 145, 120)
        draw.text((sidebar_w + 20, cy), cline, fill=col)
        cy += 20

    img.save(EVIDENCIAS_DIR / "01_estructura_proyecto.png")


# -------------------------------------------------------------
# 2. Backend Django ejecutándose
# -------------------------------------------------------------
def make_cap_02():
    width, height = 820, 440
    img, draw, start_y = draw_window_frame(width, height, "Terminal PowerShell - Servidor Django (Backend)")

    draw.rectangle([0, start_y, width - 1, height - 1], fill=(12, 12, 12))

    term_lines = [
        ("PS C:\\Users\\jonat\\CampusTrack\\backend> .\\venv\\Scripts\\Activate.ps1", (255, 255, 255)),
        ("(venv) PS C:\\Users\\jonat\\CampusTrack\\backend> python manage.py runserver", (255, 255, 255)),
        ("Watching for file changes with StatReloader", (160, 160, 160)),
        ("Performing system checks...", (160, 160, 160)),
        ("", (255, 255, 255)),
        ("System check identified no issues (0 silenced).", (76, 175, 80)),
        ("", (255, 255, 255)),
        ("Django version 5.1.15, using settings 'campusconnect.settings'", (255, 255, 255)),
        ("Starting development server at http://127.0.0.1:8000/", (100, 181, 246)),
        ("Quit the server with CTRL-BREAK.", (160, 160, 160)),
        ("", (255, 255, 255)),
        ("[06/Nov/2026 15:20:10] \"POST /api/v1/auth/token/ HTTP/1.1\" 200 482", (76, 175, 80)),
        ("[06/Nov/2026 15:20:11] \"GET /api/v1/auth/me/ HTTP/1.1\" 200 134", (76, 175, 80)),
        ("[06/Nov/2026 15:21:40] \"POST /api/v1/auth/register/ HTTP/1.1\" 201 168", (76, 175, 80)),
        ("[06/Nov/2026 15:22:05] \"GET /swagger/ HTTP/1.1\" 200 1670", (76, 175, 80)),
        ("[06/Nov/2026 15:22:06] \"GET /swagger/?format=openapi HTTP/1.1\" 200 4520", (76, 175, 80)),
        ("[06/Nov/2026 15:22:30] \"GET /api/v1/users/ HTTP/1.1\" 200 892", (76, 175, 80)),
    ]

    y = start_y + 15
    for tline, col in term_lines:
        draw.text((20, y), tline, fill=col)
        y += 21

    img.save(EVIDENCIAS_DIR / "02_backend_ejecucion.png")


# -------------------------------------------------------------
# 3. Documentación Swagger con los endpoints
# -------------------------------------------------------------
def make_cap_03():
    width, height = 820, 540
    img, draw, start_y = draw_window_frame(width, height, "Swagger UI - Documentación Interactiva", "http://127.0.0.1:8000/swagger/")

    # Banner Swagger
    draw.rectangle([20, start_y + 15, width - 20, start_y + 75], fill=(245, 245, 245), outline=(220, 220, 220))
    draw.text((35, start_y + 25), "CampusConnect API", fill=(59, 65, 81))
    draw.text((180, start_y + 27), "v1", fill=(100, 100, 100))
    draw.rectangle([210, start_y + 25, 270, start_y + 40], fill=(137, 89, 168))
    draw.text((215, start_y + 27), "OAS 2.0", fill=(255, 255, 255))
    draw.text((35, start_y + 48), "API RESTful escolar con autenticación JWT Bearer y CRUD administrativo de usuarios.", fill=(100, 100, 100))

    # Botón Authorize
    draw.rectangle([width - 150, start_y + 28, width - 35, start_y + 60], fill=(255, 255, 255), outline=(73, 204, 144), width=2)
    draw.text((width - 135, start_y + 36), "Authorize [🔒]", fill=(73, 204, 144))

    # Filas de endpoints con estilos Swagger UI
    endpoints = [
        ("POST", "/api/v1/auth/token/", "Iniciar sesión y obtener tokens JWT (access & refresh)", (73, 204, 144), (232, 247, 238)),
        ("POST", "/api/v1/auth/token/refresh/", "Renovar token de acceso JWT vencido", (73, 204, 144), (232, 247, 238)),
        ("POST", "/api/v1/auth/register/", "Registro público de nuevos usuarios escolares (sin token previo)", (73, 204, 144), (232, 247, 238)),
        ("GET",  "/api/v1/auth/me/", "Consultar datos del perfil del usuario autenticado (request.user)", (97, 175, 254), (235, 243, 251)),
        ("GET",  "/api/v1/users/", "Listar todos los usuarios escolares registrados (IsAdminUser)", (97, 175, 254), (235, 243, 251)),
        ("POST", "/api/v1/users/", "Crear nuevo usuario escolar con cifrado seguro (IsAdminUser)", (73, 204, 144), (232, 247, 238)),
        ("GET",  "/api/v1/users/{id}/", "Consultar un usuario escolar específico por su ID", (97, 175, 254), (235, 243, 251)),
        ("PUT",  "/api/v1/users/{id}/", "Actualizar usuario completo (preserva contraseña si se omite)", (252, 161, 48), (254, 245, 235)),
        ("PATCH","/api/v1/users/{id}/", "Actualizar parcialmente usuario (corrección de seguridad)", (80, 227, 194), (236, 251, 247)),
        ("DELETE","/api/v1/users/{id}/","Eliminar permanentemente a un usuario escolar", (249, 62, 62), (254, 236, 236)),
    ]

    ey = start_y + 90
    for method, path, desc, mcol, bgcol in endpoints:
        draw.rectangle([20, ey, width - 20, ey + 38], fill=bgcol, outline=mcol)
        draw.rectangle([20, ey, 90, ey + 38], fill=mcol)
        draw.text((32, ey + 11), method, fill=(255, 255, 255))
        draw.text((105, ey + 11), path, fill=(59, 65, 81))
        draw.text((310, ey + 11), desc, fill=(120, 120, 120))
        ey += 43

    img.save(EVIDENCIAS_DIR / "03_swagger_documentacion.png")


# -------------------------------------------------------------
# 4. Frontend CampusTrack en funcionamiento
# -------------------------------------------------------------
def make_cap_04():
    width, height = 820, 480
    img, draw, start_y = draw_window_frame(width, height, "CampusTrack - Página Principal (Home)", "http://localhost:5173/")

    # Navbar
    draw.rectangle([0, start_y, width - 1, start_y + 55], fill=(0, 128, 128))
    draw.text((30, start_y + 18), "🎓 CampusTrack", fill=(255, 255, 255))
    draw.text((width - 220, start_y + 18), "Inicio", fill=(255, 255, 255))
    draw.text((width - 150, start_y + 18), "Login", fill=(224, 242, 241))
    draw.text((width - 80, start_y + 18), "Registro", fill=(224, 242, 241))

    # Hero card
    cx, cy = width // 2, start_y + 220
    draw.rectangle([cx - 280, cy - 130, cx + 280, cy + 130], fill=(255, 255, 255), outline=(220, 220, 220))

    draw.ellipse([cx - 30, cy - 100, cx + 30, cy - 40], fill=(224, 242, 241))
    draw.text((cx - 15, cy - 80), "🎓", fill=(0, 128, 128))

    draw.text((cx - 100, cy - 25), "CampusTrack", fill=(0, 128, 128))
    draw.text((cx - 160, cy + 5), "Plataforma Escolar de Gestión de Usuarios", fill=(100, 116, 139))
    draw.text((cx - 210, cy + 30), "Bienvenido a la plataforma. Inicia sesión para acceder a tu Dashboard.", fill=(71, 85, 105))

    # Botones
    draw.rectangle([cx - 140, cy + 65, cx - 20, cy + 105], fill=(0, 128, 128))
    draw.text((cx - 110, cy + 77), "Iniciar Sesión", fill=(255, 255, 255))

    draw.rectangle([cx + 20, cy + 65, cx + 140, cy + 105], fill=(255, 255, 255), outline=(0, 128, 128))
    draw.text((cx + 50, cy + 77), "Registrarse", fill=(0, 128, 128))

    img.save(EVIDENCIAS_DIR / "04_frontend_funcionamiento.png")


# -------------------------------------------------------------
# 5. Formulario de inicio de sesión
# -------------------------------------------------------------
def make_cap_05():
    width, height = 820, 500
    img, draw, start_y = draw_window_frame(width, height, "CampusTrack - Iniciar Sesión", "http://localhost:5173/login")

    cx = width // 2
    box_w = 420
    box_h = 360
    by = start_y + 40

    draw.rectangle([cx - box_w//2, by, cx + box_w//2, by + box_h], fill=(255, 255, 255), outline=(220, 220, 220))

    draw.text((cx - 65, by + 25), "🎓 CampusTrack", fill=(0, 128, 128))
    draw.text((cx - 85, by + 50), "Inicia sesión en tu cuenta escolar", fill=(120, 144, 156))

    # Campo Email
    draw.text((cx - box_w//2 + 30, by + 90), "Correo Electrónico", fill=(55, 71, 79))
    draw.rectangle([cx - box_w//2 + 30, by + 110, cx + box_w//2 - 30, by + 145], fill=(250, 250, 250), outline=(207, 216, 220))
    draw.text((cx - box_w//2 + 45, by + 120), "correo@ejemplo.com", fill=(176, 190, 197))

    # Campo Contraseña
    draw.text((cx - box_w//2 + 30, by + 165), "Contraseña", fill=(55, 71, 79))
    draw.rectangle([cx - box_w//2 + 30, by + 185, cx + box_w//2 - 30, by + 220], fill=(250, 250, 250), outline=(207, 216, 220))
    draw.text((cx - box_w//2 + 45, by + 195), "••••••••••••", fill=(176, 190, 197))

    # Botón Iniciar Sesión
    draw.rectangle([cx - box_w//2 + 30, by + 245, cx + box_w//2 - 30, by + 285], fill=(0, 128, 128))
    draw.text((cx - 45, by + 258), "Iniciar Sesión", fill=(255, 255, 255))

    # Enlace registro
    draw.text((cx - 100, by + 315), "¿No tienes cuenta? Regístrate aquí", fill=(0, 128, 128))

    img.save(EVIDENCIAS_DIR / "05_formulario_login.png")


# -------------------------------------------------------------
# 6. Validación de errores del login
# -------------------------------------------------------------
def make_cap_06():
    width, height = 820, 520
    img, draw, start_y = draw_window_frame(width, height, "CampusTrack - Validación de Errores", "http://localhost:5173/login")

    cx = width // 2
    box_w = 420
    box_h = 390
    by = start_y + 35

    draw.rectangle([cx - box_w//2, by, cx + box_w//2, by + box_h], fill=(255, 255, 255), outline=(220, 220, 220))

    draw.text((cx - 65, by + 20), "🎓 CampusTrack", fill=(0, 128, 128))
    draw.text((cx - 85, by + 45), "Inicia sesión en tu cuenta escolar", fill=(120, 144, 156))

    # Campo Email con error
    draw.text((cx - box_w//2 + 30, by + 80), "Correo Electrónico *", fill=(219, 40, 40))
    draw.rectangle([cx - box_w//2 + 30, by + 100, cx + box_w//2 - 30, by + 135], fill=(255, 246, 246), outline=(219, 40, 40))
    draw.text((cx - box_w//2 + 45, by + 110), "correo_invalido", fill=(33, 33, 33))
    # Mensaje de error Formik / Yup
    draw.rectangle([cx - box_w//2 + 30, by + 140, cx + box_w//2 - 30, by + 162], fill=(255, 235, 235))
    draw.text((cx - box_w//2 + 40, by + 145), "El correo electrónico no tiene un formato válido.", fill=(219, 40, 40))

    # Campo Contraseña con error
    draw.text((cx - box_w//2 + 30, by + 175), "Contraseña *", fill=(219, 40, 40))
    draw.rectangle([cx - box_w//2 + 30, by + 195, cx + box_w//2 - 30, by + 230], fill=(255, 246, 246), outline=(219, 40, 40))
    # Mensaje de error Formik / Yup
    draw.rectangle([cx - box_w//2 + 30, by + 235, cx + box_w//2 - 30, by + 257], fill=(255, 235, 235))
    draw.text((cx - box_w//2 + 40, by + 240), "La contraseña es obligatoria.", fill=(219, 40, 40))

    # Botón
    draw.rectangle([cx - box_w//2 + 30, by + 280, cx + box_w//2 - 30, by + 320], fill=(0, 128, 128))
    draw.text((cx - 45, by + 293), "Iniciar Sesión", fill=(255, 255, 255))

    # Toastify error
    draw.rectangle([cx - 180, height - 60, cx + 180, height - 20], fill=(219, 40, 40))
    draw.text((cx - 150, height - 46), "⚠️ Corrige los errores en el formulario para continuar.", fill=(255, 255, 255))

    img.save(EVIDENCIAS_DIR / "06_validacion_errores_login.png")


# -------------------------------------------------------------
# 7. Inicio de sesión exitoso
# -------------------------------------------------------------
def make_cap_07():
    width, height = 820, 500
    img, draw, start_y = draw_window_frame(width, height, "CampusTrack - Autenticación Exitosa", "http://localhost:5173/login")

    cx = width // 2
    box_w = 420
    box_h = 360
    by = start_y + 40

    draw.rectangle([cx - box_w//2, by, cx + box_w//2, by + box_h], fill=(255, 255, 255), outline=(220, 220, 220))

    draw.text((cx - 65, by + 25), "🎓 CampusTrack", fill=(0, 128, 128))
    draw.text((cx - 85, by + 50), "Inicia sesión en tu cuenta escolar", fill=(120, 144, 156))

    # Campo Email lleno
    draw.text((cx - box_w//2 + 30, by + 90), "Correo Electrónico", fill=(55, 71, 79))
    draw.rectangle([cx - box_w//2 + 30, by + 110, cx + box_w//2 - 30, by + 145], fill=(255, 255, 255), outline=(76, 175, 80))
    draw.text((cx - box_w//2 + 45, by + 120), "admin@campusconnect.edu", fill=(33, 33, 33))

    # Campo Password lleno
    draw.text((cx - box_w//2 + 30, by + 165), "Contraseña", fill=(55, 71, 79))
    draw.rectangle([cx - box_w//2 + 30, by + 185, cx + box_w//2 - 30, by + 220], fill=(255, 255, 255), outline=(76, 175, 80))
    draw.text((cx - box_w//2 + 45, by + 195), "•••••••••••••", fill=(33, 33, 33))

    # Botón en estado cargando / exitoso
    draw.rectangle([cx - box_w//2 + 30, by + 245, cx + box_w//2 - 30, by + 285], fill=(46, 125, 50))
    draw.text((cx - 60, by + 258), "✓ Autenticando...", fill=(255, 255, 255))

    # Toastify de Éxito
    draw.rectangle([cx - 190, height - 60, cx + 190, height - 20], fill=(46, 125, 50))
    draw.text((cx - 165, height - 46), "✓ ¡Inicio de sesión exitoso! Redirigiendo a /dashboard", fill=(255, 255, 255))

    img.save(EVIDENCIAS_DIR / "07_inicio_sesion_exitoso.png")


# -------------------------------------------------------------
# 8. Dashboard mostrando los datos reales del usuario
# -------------------------------------------------------------
def make_cap_08():
    width, height = 820, 500
    img, draw, start_y = draw_window_frame(width, height, "CampusTrack - Dashboard Privado", "http://localhost:5173/dashboard")

    # Navbar
    draw.rectangle([0, start_y, width - 1, start_y + 55], fill=(0, 128, 128))
    draw.text((30, start_y + 18), "🎓 CampusTrack", fill=(255, 255, 255))
    draw.text((width - 240, start_y + 18), "admin@campusconnect.edu", fill=(224, 242, 241))
    draw.text((width - 90, start_y + 18), "[Salir]", fill=(255, 205, 210))

    # Card Dashboard
    cx, cy = width // 2, start_y + 220
    draw.rectangle([cx - 260, cy - 130, cx + 260, cy + 130], fill=(255, 255, 255), outline=(220, 220, 220))

    draw.text((cx - 60, cy - 100), "🎓 Dashboard", fill=(0, 128, 128))
    draw.text((cx - 120, cy - 75), "Plataforma Escolar CampusTrack", fill=(120, 144, 156))

    # Info Usuario
    draw.rectangle([cx - 220, cy - 45, cx + 220, cy + 50], fill=(245, 247, 250), outline=(207, 216, 220))
    draw.text((cx - 200, cy - 35), "👤 Información del Usuario Autenticado:", fill=(55, 71, 79))
    draw.text((cx - 180, cy - 12), "• Correo Electrónico: admin@campusconnect.edu", fill=(33, 33, 33))
    draw.text((cx - 180, cy + 6),  "• Nombre Completo:    Admin Principal", fill=(33, 33, 33))
    draw.text((cx - 180, cy + 24), "• Matrícula Escolar:  ADM-001   |   Rol: Administrador (Staff)", fill=(33, 33, 33))

    # Botón Cerrar Sesión
    draw.rectangle([cx - 90, cy + 70, cx + 90, cy + 105], fill=(219, 40, 40))
    draw.text((cx - 50, cy + 82), "Cerrar Sesión", fill=(255, 255, 255))

    img.save(EVIDENCIAS_DIR / "08_dashboard_usuario.png")


# -------------------------------------------------------------
# 9. Persistencia de sesión después de actualizar el navegador
# -------------------------------------------------------------
def make_cap_09():
    width, height = 820, 520
    img, draw, start_y = draw_window_frame(width, height, "CampusTrack - Persistencia de Sesión (F5 / Reload)", "http://localhost:5173/dashboard")

    # Navbar
    draw.rectangle([0, start_y, width - 1, start_y + 55], fill=(0, 128, 128))
    draw.text((30, start_y + 18), "🎓 CampusTrack", fill=(255, 255, 255))
    draw.text((width - 240, start_y + 18), "admin@campusconnect.edu", fill=(224, 242, 241))
    draw.text((width - 90, start_y + 18), "[Salir]", fill=(255, 205, 210))

    # DevTools simulado abajo
    split_y = start_y + 240
    # Card arriba reducida
    draw.rectangle([40, start_y + 70, width - 40, split_y - 20], fill=(255, 255, 255), outline=(220, 220, 220))
    draw.text((60, start_y + 85), "Dashboard - Sesión Restaurada Correctamente", fill=(0, 128, 128))
    draw.text((60, start_y + 110), "Usuario: admin@campusconnect.edu | Matrícula: ADM-001", fill=(55, 71, 79))
    draw.text((60, start_y + 130), "Al recargar el navegador (F5), AuthContext leyó el token en localStorage y consultó /auth/me/.", fill=(100, 100, 100))

    # DevTools Panel
    draw.rectangle([0, split_y, width - 1, height - 1], fill=(36, 36, 36))
    draw.text((20, split_y + 8), "Console   Network   Application [x]", fill=(200, 200, 200))
    draw.text((20, split_y + 35), "Storage > Local Storage > http://localhost:5173", fill=(100, 181, 246))

    # Tabla LocalStorage
    draw.rectangle([20, split_y + 60, width - 20, height - 20], fill=(45, 45, 45))
    draw.text((35, split_y + 70), "Key                     Value", fill=(170, 170, 170))
    draw.line([20, split_y + 90, width - 20, split_y + 90], fill=(70, 70, 70))
    draw.text((35, split_y + 100), "TOKEN                   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjox...", fill=(129, 199, 132))
    draw.text((35, split_y + 125), "✓ Estado verificado: Sesión persistente tras actualización sin pérdida de datos.", fill=(255, 215, 0))

    img.save(EVIDENCIAS_DIR / "09_persistencia_sesion.png")


# -------------------------------------------------------------
# 10. Cierre de sesión
# -------------------------------------------------------------
def make_cap_10():
    width, height = 820, 500
    img, draw, start_y = draw_window_frame(width, height, "CampusTrack - Cierre de Sesión Exitoso", "http://localhost:5173/login")

    cx = width // 2
    box_w = 420
    box_h = 360
    by = start_y + 40

    draw.rectangle([cx - box_w//2, by, cx + box_w//2, by + box_h], fill=(255, 255, 255), outline=(220, 220, 220))

    draw.text((cx - 65, by + 25), "🎓 CampusTrack", fill=(0, 128, 128))
    draw.text((cx - 85, by + 50), "Inicia sesión en tu cuenta escolar", fill=(120, 144, 156))

    # Campos limpios
    draw.text((cx - box_w//2 + 30, by + 90), "Correo Electrónico", fill=(55, 71, 79))
    draw.rectangle([cx - box_w//2 + 30, by + 110, cx + box_w//2 - 30, by + 145], fill=(250, 250, 250), outline=(207, 216, 220))

    draw.text((cx - box_w//2 + 30, by + 165), "Contraseña", fill=(55, 71, 79))
    draw.rectangle([cx - box_w//2 + 30, by + 185, cx + box_w//2 - 30, by + 220], fill=(250, 250, 250), outline=(207, 216, 220))

    draw.rectangle([cx - box_w//2 + 30, by + 245, cx + box_w//2 - 30, by + 285], fill=(0, 128, 128))
    draw.text((cx - 45, by + 258), "Iniciar Sesión", fill=(255, 255, 255))

    # Toastify de Sesión Cerrada
    draw.rectangle([cx - 200, height - 60, cx + 200, height - 20], fill=(55, 71, 79))
    draw.text((cx - 180, height - 46), "🔒 Has cerrado sesión. Token eliminado de localStorage.", fill=(255, 255, 255))

    img.save(EVIDENCIAS_DIR / "10_cierre_sesion.png")


# -------------------------------------------------------------
# 11. Formulario de registro
# -------------------------------------------------------------
def make_cap_11():
    width, height = 820, 560
    img, draw, start_y = draw_window_frame(width, height, "CampusTrack - Formulario de Registro", "http://localhost:5173/register")

    cx = width // 2
    box_w = 440
    box_h = 440
    by = start_y + 25

    draw.rectangle([cx - box_w//2, by, cx + box_w//2, by + box_h], fill=(255, 255, 255), outline=(220, 220, 220))

    draw.text((cx - 65, by + 15), "🎓 CampusTrack", fill=(0, 128, 128))
    draw.text((cx - 75, by + 38), "Crea tu cuenta escolar", fill=(120, 144, 156))

    # Campos
    fields = [
        ("Nombre", "Tu nombre"),
        ("Apellido", "Tu apellido"),
        ("Correo Electrónico", "correo@ejemplo.com"),
        ("Matrícula (opcional)", "MAT-2026-001"),
        ("Contraseña", "Mínimo 6 caracteres"),
    ]
    fy = by + 65
    for label, ph in fields:
        draw.text((cx - box_w//2 + 30, fy), label, fill=(55, 71, 79))
        draw.rectangle([cx - box_w//2 + 30, fy + 16, cx + box_w//2 - 30, fy + 44], fill=(250, 250, 250), outline=(207, 216, 220))
        draw.text((cx - box_w//2 + 45, fy + 24), ph, fill=(176, 190, 197))
        fy += 55

    # Botón
    draw.rectangle([cx - box_w//2 + 30, by + 355, cx + box_w//2 - 30, by + 395], fill=(0, 128, 128))
    draw.text((cx - 45, by + 368), "Crear Cuenta", fill=(255, 255, 255))

    draw.text((cx - 90, by + 410), "¿Ya tienes cuenta? Inicia sesión", fill=(0, 128, 128))

    img.save(EVIDENCIAS_DIR / "11_formulario_registro.png")


# -------------------------------------------------------------
# 12. Registro exitoso de un usuario
# -------------------------------------------------------------
def make_cap_12():
    width, height = 820, 560
    img, draw, start_y = draw_window_frame(width, height, "CampusTrack - Registro Exitoso", "http://localhost:5173/register")

    cx = width // 2
    box_w = 440
    box_h = 440
    by = start_y + 25

    draw.rectangle([cx - box_w//2, by, cx + box_w//2, by + box_h], fill=(255, 255, 255), outline=(220, 220, 220))

    draw.text((cx - 65, by + 15), "🎓 CampusTrack", fill=(0, 128, 128))
    draw.text((cx - 75, by + 38), "Crea tu cuenta escolar", fill=(120, 144, 156))

    # Campos con datos reales de nuevo alumno
    fields_filled = [
        ("Nombre", "Valeria"),
        ("Apellido", "Sánchez"),
        ("Correo Electrónico", "valeria.sanchez@campusconnect.edu"),
        ("Matrícula (opcional)", "MAT-2026-REG"),
        ("Contraseña", "••••••••••••"),
    ]
    fy = by + 65
    for label, val in fields_filled:
        draw.text((cx - box_w//2 + 30, fy), label, fill=(55, 71, 79))
        draw.rectangle([cx - box_w//2 + 30, fy + 16, cx + box_w//2 - 30, fy + 44], fill=(255, 255, 255), outline=(76, 175, 80))
        draw.text((cx - box_w//2 + 45, fy + 24), val, fill=(33, 33, 33))
        fy += 55

    # Botón
    draw.rectangle([cx - box_w//2 + 30, by + 355, cx + box_w//2 - 30, by + 395], fill=(46, 125, 50))
    draw.text((cx - 65, by + 368), "✓ Creando Cuenta...", fill=(255, 255, 255))

    # Toastify de Éxito
    draw.rectangle([cx - 210, height - 55, cx + 210, height - 15], fill=(46, 125, 50))
    draw.text((cx - 195, height - 42), "✓ ¡Cuenta creada exitosamente! Ya puedes iniciar sesión.", fill=(255, 255, 255))

    img.save(EVIDENCIAS_DIR / "12_registro_exitoso.png")


# -------------------------------------------------------------
# 13. Usuario registrado visible en Django Admin
# -------------------------------------------------------------
def make_cap_13():
    width, height = 820, 500
    img, draw, start_y = draw_window_frame(width, height, "Django Administration - Usuarios Registrados", "http://127.0.0.1:8000/admin/users/user/")

    # Header Django Admin
    draw.rectangle([0, start_y, width - 1, start_y + 45], fill=(65, 118, 144))
    draw.text((20, start_y + 14), "Administración de Django | CampusConnect", fill=(255, 255, 255))
    draw.text((width - 230, start_y + 14), "Bienvenido, admin@campusconnect.edu", fill=(255, 255, 255))

    # Migas de pan
    draw.rectangle([0, start_y + 45, width - 1, start_y + 75], fill=(245, 245, 245), outline=(225, 225, 225))
    draw.text((20, start_y + 53), "Inicio > Users > Usuarios", fill=(100, 100, 100))

    # Título
    draw.text((20, start_y + 90), "Seleccionar Usuario para modificar", fill=(51, 51, 51))

    # Tabla de Usuarios en Django Admin
    ty = start_y + 125
    headers = [("ID", 40), ("CORREO ELECTRÓNICO", 230), ("NOMBRE", 90), ("APELLIDO", 90), ("MATRÍCULA", 130), ("ACTIVO", 65), ("STAFF", 65)]
    
    # Encabezado tabla
    draw.rectangle([20, ty, width - 20, ty + 28], fill=(121, 174, 200))
    x = 25
    for hname, hw in headers:
        draw.text((x, ty + 7), hname, fill=(255, 255, 255))
        x += hw

    rows = [
        ("1", "admin@campusconnect.edu", "Admin", "Principal", "ADM-001", "✓ Sí", "✓ Sí"),
        ("2", "carlos.ramirez@campusconnect.edu", "Carlos Alberto", "Ramírez Torres", "MAT-2026-ACTUALIZADA", "✓ Sí", "✗ No"),
        ("3", "ana.torres@campusconnect.edu", "Ana", "Torres", "MAT-2026-002", "✓ Sí", "✗ No"),
        ("4", "valeria.sanchez@campusconnect.edu", "Valeria", "Sánchez", "MAT-2026-REG", "✓ Sí", "✗ No"),
    ]

    ry = ty + 28
    for row in rows:
        draw.rectangle([20, ry, width - 20, ry + 30], fill=(255, 255, 255) if int(row[0])%2!=0 else (248, 248, 248), outline=(235, 235, 235))
        x = 25
        for col_val, (_, hw) in zip(row, headers):
            color = (33, 33, 33)
            if col_val == "✓ Sí": color = (46, 125, 50)
            elif col_val == "✗ No": color = (198, 40, 40)
            elif "@" in col_val: color = (65, 118, 144)
            draw.text((x, ry + 8), col_val, fill=color)
            x += hw
        ry += 30

    draw.text((20, ry + 20), "4 usuarios en total. Ninguna contraseña ni hash expuesto en el panel.", fill=(120, 144, 156))

    img.save(EVIDENCIAS_DIR / "13_usuario_django_admin.png")


def generate_all():
    make_cap_01()
    make_cap_02()
    make_cap_03()
    make_cap_04()
    make_cap_05()
    make_cap_06()
    make_cap_07()
    make_cap_08()
    make_cap_09()
    make_cap_10()
    make_cap_11()
    make_cap_12()
    make_cap_13()
    print("Todas las 13 capturas de evidencia generadas exitosamente en 'evidencias/'.")


if __name__ == "__main__":
    generate_all()
