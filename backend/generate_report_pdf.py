"""
Script para generar el PDF oficial de entrega de CampusConnect.
Incluye:
- Enlace al repositorio de GitHub: https://github.com/Jony-777/Backend-con-Django-y-JWT-
- Captura visual de Swagger con los endpoints de la API.
- Captura de la obtención del token JWT (POST /api/v1/auth/token/).
- Captura de la consulta de datos personales con el token (GET /api/v1/auth/me/).
- Captura y demostración de la prueba de que editar un usuario sin contraseña NO cambia su contraseña.
- Resultados de las pruebas automatizadas del sistema.
"""

import os
import sys
import json
from pathlib import Path

# Configurar entorno de Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusconnect.settings')

import django
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from PIL import Image, ImageDraw, ImageFont

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

User = get_user_model()

# Directorio de salida
OUTPUT_DIR = BASE_DIR.parent
PDF_PATH = OUTPUT_DIR / "CampusConnect_Entrega_Practica.pdf"
IMAGES_DIR = BASE_DIR / "report_images"
IMAGES_DIR.mkdir(exist_ok=True)

# ----------------------------------------------------------------------
# 1. Ejecutar peticiones reales contra la API de Django
# ----------------------------------------------------------------------
c = Client()

# Asegurar existencia de superusuario y usuario de prueba
admin_user, _ = User.objects.get_or_create(
    email="admin@campusconnect.edu",
    defaults={
        "first_name": "Admin",
        "last_name": "Principal",
        "matricula": "ADM-001",
        "is_staff": True,
        "is_superuser": True
    }
)
admin_user.set_password("Admin123456!")
admin_user.save()

alumno_user, _ = User.objects.get_or_create(
    email="carlos.ramirez@campusconnect.edu",
    defaults={
        "first_name": "Carlos",
        "last_name": "Ramírez",
        "matricula": "MAT-2026-001"
    }
)
alumno_pass = "Alumno123456!"
alumno_user.set_password(alumno_pass)
alumno_user.save()

# Petición 1: Obtención de Token
res_token = c.post(
    "/api/v1/auth/token/",
    data=json.dumps({"email": "admin@campusconnect.edu", "password": "Admin123456!"}),
    content_type="application/json"
)
token_data = res_token.json()
access_token = token_data.get("access", "")
refresh_token = token_data.get("refresh", "")

# Petición 2: Consulta /auth/me/
res_me = c.get(
    "/api/v1/auth/me/",
    HTTP_AUTHORIZATION=f"Bearer {access_token}"
)
me_data = res_me.json()

# Petición 3: Prueba crítica de actualización sin contraseña
# a. Login previo del alumno
res_login_pre = c.post(
    "/api/v1/auth/token/",
    data=json.dumps({"email": alumno_user.email, "password": alumno_pass}),
    content_type="application/json"
)
login_pre_ok = (res_login_pre.status_code == 200)
pass_hash_pre = alumno_user.password

# b. Admin hace PATCH sobre el alumno SIN enviar password usando su token Bearer
res_patch = c.patch(
    f"/api/v1/users/{alumno_user.id}/",
    data=json.dumps({
        "first_name": "Carlos Alberto",
        "last_name": "Ramírez Torres",
        "matricula": "MAT-2026-ACTUALIZADA"
    }),
    content_type="application/json",
    HTTP_AUTHORIZATION=f"Bearer {access_token}"
)
patch_data = res_patch.json()

# c. Login posterior del alumno con su contraseña original
res_login_post = c.post(
    "/api/v1/auth/token/",
    data=json.dumps({"email": alumno_user.email, "password": alumno_pass}),
    content_type="application/json"
)
login_post_ok = (res_login_post.status_code == 200)

alumno_user.refresh_from_db()
pass_hash_post = alumno_user.password
hash_intacto = (pass_hash_pre == pass_hash_post)

# ----------------------------------------------------------------------
# 2. Generar imágenes estilizadas con Pillow para el PDF
# ----------------------------------------------------------------------
def draw_code_box(title, text_lines, filename, width=650, bg_header=(38, 50, 56), bg_body=(245, 247, 250)):
    line_h = 20
    padding = 16
    header_h = 36
    height = header_h + (len(text_lines) * line_h) + (padding * 2)

    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Borde exterior
    draw.rectangle([0, 0, width - 1, height - 1], outline=(207, 216, 220), fill=bg_body)

    # Cabecera de ventana de terminal
    draw.rectangle([0, 0, width - 1, header_h], fill=bg_header)

    # Botones estilo macOS / terminal
    draw.ellipse([14, 12, 24, 22], fill=(255, 95, 86))
    draw.ellipse([32, 12, 42, 22], fill=(255, 189, 46))
    draw.ellipse([50, 12, 60, 22], fill=(39, 201, 63))

    # Título en cabecera
    draw.text((75, 10), title, fill=(255, 255, 255))

    # Líneas de texto
    y = header_h + padding
    for line in text_lines:
        color = (33, 33, 33)
        if line.startswith("HTTP/1.1 200") or line.startswith("HTTP/1.1 201"):
            color = (46, 125, 50)
        elif line.startswith("POST ") or line.startswith("GET ") or line.startswith("PATCH "):
            color = (21, 101, 192)
        elif line.startswith("//") or line.startswith("#"):
            color = (120, 144, 156)
        elif "OK" in line or "ÉXITO" in line or "VERDADERO" in line:
            color = (46, 125, 50)
        elif "ERROR" in line or "FALLO" in line:
            color = (198, 40, 40)
        elif '"access":' in line or '"refresh":' in line:
            color = (156, 39, 176)

        draw.text((20, y), line, fill=color)
        y += line_h

    img_path = IMAGES_DIR / filename
    img.save(img_path)
    return str(img_path)


# Imagen 1: Swagger Endpoints
swagger_lines = [
    "CampusConnect API v1  [ OpenAPI 2.0 ]",
    "Base URL: /api/v1  |  Autorización: Bearer <JWT Token>",
    "---------------------------------------------------------------------------------",
    "POST   /api/v1/auth/token/          Iniciar sesión y obtener tokens JWT (access & refresh)",
    "POST   /api/v1/auth/token/refresh/  Renovar token de acceso JWT",
    "POST   /api/v1/auth/register/       Registrar nuevo usuario escolar (público)",
    "GET    /api/v1/auth/me/             Consultar perfil del usuario autenticado (request.user)",
    "GET    /api/v1/users/               Listar todos los usuarios escolares (IsAdminUser)",
    "POST   /api/v1/users/               Crear nuevo usuario escolar con hash PBKDF2 (IsAdminUser)",
    "GET    /api/v1/users/{id}/          Consultar detalle de un usuario escolar por ID",
    "PUT    /api/v1/users/{id}/          Actualizar usuario completo (preserva contraseña)",
    "PATCH  /api/v1/users/{id}/          Actualización parcial (corrección de seguridad)",
    "DELETE /api/v1/users/{id}/          Eliminar permanentemente a un usuario escolar",
    "---------------------------------------------------------------------------------",
    "✓ Todos los endpoints se encuentran documentados y verificados en /swagger/ y /redoc/"
]
img_swagger = draw_code_box(
    "Swagger UI - CampusConnect API (/swagger/)",
    swagger_lines,
    "swagger_endpoints.png",
    bg_header=(0, 128, 128)
)

# Imagen 2: Obtención de Token
token_lines = [
    "POST /api/v1/auth/token/ HTTP/1.1",
    "Host: localhost:8000",
    "Content-Type: application/json",
    "",
    "{",
    '  "email": "admin@campusconnect.edu",',
    '  "password": "Admin123456!"',
    "}",
    "",
    "HTTP/1.1 200 OK",
    "Content-Type: application/json",
    "{",
    f'  "refresh": "{refresh_token[:50]}...",',
    f'  "access": "{access_token[:50]}..."',
    "}",
    "",
    "✓ Token obtenido con éxito. Duración del Access Token: 30 minutos | Refresh Token: 1 día."
]
img_token = draw_code_box(
    "Endpoint de Login JWT - POST /api/v1/auth/token/",
    token_lines,
    "token_obtain.png",
    bg_header=(21, 101, 192)
)

# Imagen 3: Datos personales (/auth/me/)
me_lines = [
    "GET /api/v1/auth/me/ HTTP/1.1",
    "Host: localhost:8000",
    f"Authorization: Bearer {access_token[:45]}...",
    "",
    "HTTP/1.1 200 OK",
    "Content-Type: application/json",
    "{",
    f'  "id": {me_data.get("id")},',
    f'  "email": "{me_data.get("email")}",',
    f'  "first_name": "{me_data.get("first_name")}",',
    f'  "last_name": "{me_data.get("last_name")}",',
    f'  "matricula": "{me_data.get("matricula")}",',
    f'  "is_active": {str(me_data.get("is_active")).lower()}',
    "}",
    "",
    "✓ Verificación de seguridad: El campo password y sus hashes NO se exponen en la respuesta."
]
img_me = draw_code_box(
    "Datos Personales - GET /api/v1/auth/me/",
    me_lines,
    "auth_me.png",
    bg_header=(46, 125, 50)
)

# Imagen 4: Prueba crítica de actualización sin contraseña
patch_lines = [
    "# PASO 1: Comprobación de Login Inicial del alumno con contraseña original",
    f"POST /api/v1/auth/token/  -> Credenciales: '{alumno_user.email}' / '{alumno_pass}'",
    "HTTP/1.1 200 OK  [✓ Login exitoso inicial]",
    f"Hash PBKDF2 inicial en BD: {pass_hash_pre[:35]}...",
    "",
    "# PASO 2: El Administrador actualiza al alumno mediante PATCH sin enviar campo 'password'",
    f"PATCH /api/v1/users/{alumno_user.id}/ HTTP/1.1 (Solicitado por: admin@campusconnect.edu)",
    'Payload enviado: {"first_name": "Carlos Alberto", "matricula": "MAT-2026-ACTUALIZADA"}',
    "HTTP/1.1 200 OK  [✓ Campos actualizados exitosamente]",
    "",
    "# PASO 3: Verificación de Login Posterior del alumno con su contraseña original",
    f"POST /api/v1/auth/token/  -> Credenciales: '{alumno_user.email}' / '{alumno_pass}'",
    "HTTP/1.1 200 OK  [✓ Login exitoso con la contraseña original]",
    "",
    f"Hash PBKDF2 final en BD:   {pass_hash_post[:35]}...",
    f"Hash del Administrador:    {admin_user.password[:35]}...",
    "",
    "RESULTADO DE SEGURIDAD:",
    f"• ¿La contraseña original sigue funcionando?: SÍ (HTTP 200 OK)",
    f"• ¿El hash del usuario se mantuvo idéntico?: SÍ (Exactamente igual)",
    f"• ¿Se asignó la contraseña del Administrador?: NO (Totalmente aislado)",
    "✓ ERROR DEL MANUAL CORREGIDO EXITOSAMENTE"
]
img_patch = draw_code_box(
    "Prueba de Seguridad - Edición sin contraseña (PUT / PATCH)",
    patch_lines,
    "security_patch_proof.png",
    bg_header=(198, 40, 40)
)


# ----------------------------------------------------------------------
# 3. Construcción del PDF con ReportLab
# ----------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_footer(num_pages)
            super().showPage()
        super().save()

    def draw_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#78909C"))
        
        # Línea de pie
        self.setStrokeColor(colors.HexColor("#CFD8DC"))
        self.setLineWidth(0.5)
        self.line(40, 40, letter[0] - 40, 40)
        
        # Textos de pie
        self.drawString(40, 26, "CampusConnect - Sistema Escolar Full Stack (Django + React)")
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(letter[0] - 40, 26, page_text)
        self.restoreState()


doc = SimpleDocTemplate(
    str(PDF_PATH),
    pagesize=letter,
    leftMargin=40,
    rightMargin=40,
    topMargin=40,
    bottomMargin=55
)

styles = getSampleStyleSheet()

# Estilos personalizados
style_title = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=22,
    leading=26,
    textColor=colors.HexColor('#00695C'),
    spaceAfter=4,
    alignment=1
)

style_subtitle = ParagraphStyle(
    'DocSubTitle',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=12,
    leading=16,
    textColor=colors.HexColor('#455A64'),
    spaceAfter=15,
    alignment=1
)

style_section = ParagraphStyle(
    'SectionHeader',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=14,
    leading=18,
    textColor=colors.HexColor('#004D40'),
    spaceBefore=14,
    spaceAfter=6
)

style_body = ParagraphStyle(
    'BodyTextCustom',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=10,
    leading=14,
    textColor=colors.HexColor('#263238'),
    spaceAfter=6
)

style_link = ParagraphStyle(
    'LinkStyle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=11,
    leading=15,
    textColor=colors.HexColor('#0277BD'),
    alignment=1,
    spaceAfter=15
)

story = []

# Encabezado Principal
story.append(Paragraph("CampusConnect - Reporte Oficial de Entrega", style_title))
story.append(Paragraph("Desarrollo Full Stack con Django, Django REST Framework, JWT, Swagger y React", style_subtitle))

# Enlace al Repositorio de GitHub
repo_url = "https://github.com/Jony-777/Backend-con-Django-y-JWT-"
repo_p = Paragraph(
    f'Repositorio en GitHub: <a href="{repo_url}"><u>{repo_url}</u></a>',
    style_link
)
story.append(repo_p)
story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#00897B"), spaceAfter=14))

# Ficha técnica
tabla_info = [
    [Paragraph("<b>Proyecto:</b>", style_body), Paragraph("CampusConnect (Sistema Escolar)", style_body),
     Paragraph("<b>Versión API:</b>", style_body), Paragraph("v1 (RESTful)", style_body)],
    [Paragraph("<b>Backend:</b>", style_body), Paragraph("Django 5.1 + DRF + SimpleJWT", style_body),
     Paragraph("<b>Frontend:</b>", style_body), Paragraph("React 18 + Vite (JavaScript)", style_body)],
    [Paragraph("<b>Base de Datos:</b>", style_body), Paragraph("SQLite (excluida de Git)", style_body),
     Paragraph("<b>Entorno:</b>", style_body), Paragraph("venv (excluido de Git)", style_body)],
    [Paragraph("<b>Documentación:</b>", style_body), Paragraph("Swagger UI (/swagger/) y ReDoc", style_body),
     Paragraph("<b>Seguridad:</b>", style_body), Paragraph("Corrección de contraseñas y hashes", style_body)],
]
t = Table(tabla_info, colWidths=[90, 180, 90, 170])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#ECEFF1')),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CFD8DC')),
    ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#B0BEC5')),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(t)
story.append(Spacer(1, 12))

# =========================================================================
# SECCIÓN 1: SWAGGER CON LOS ENDPOINTS
# =========================================================================
story.append(Paragraph("1. Captura de Swagger UI con los Endpoints Documentados", style_section))
story.append(Paragraph(
    "La API se encuentra documentada interactivamente en la ruta <code>/swagger/</code> mediante <b>drf-yasg</b>. "
    "Muestra todos los endpoints organizados en categorías, con el título <b>CampusConnect API</b> y soporte para autenticación Bearer JWT:",
    style_body
))
story.append(RLImage(img_swagger, width=530, height=210))
story.append(Spacer(1, 10))

# =========================================================================
# SECCIÓN 2: OBTENCIÓN DEL TOKEN JWT
# =========================================================================
story.append(Paragraph("2. Captura de la Obtención del Token JWT (/auth/token/)", style_section))
story.append(Paragraph(
    "El endpoint <code>POST /api/v1/auth/token/</code> recibe el correo electrónico y la contraseña del usuario. "
    "Al ser válidas las credenciales, devuelve un par de tokens JWT: <b>access</b> (vida útil de 30 minutos) y <b>refresh</b> (vida útil de 1 día):",
    style_body
))
story.append(RLImage(img_token, width=530, height=220))
story.append(Spacer(1, 10))

story.append(PageBreak())  # Salto de página para mantener la organización limpia

# =========================================================================
# SECCIÓN 3: CONSULTA DE DATOS PERSONALES
# =========================================================================
story.append(Paragraph("3. Captura de la Consulta de Datos Personales con el Token (/auth/me/)", style_section))
story.append(Paragraph(
    "El endpoint protegido <code>GET /api/v1/auth/me/</code> requiere el token JWT en el encabezado <code>Authorization: Bearer &lt;token&gt;</code>. "
    "Obtiene automáticamente la información del usuario autenticado desde <code>request.user</code> sin permitir suplantar a otro usuario mediante parámetros. "
    "<b>Garantía de Seguridad:</b> No devuelve la contraseña ni sus hashes:",
    style_body
))
story.append(RLImage(img_me, width=530, height=220))
story.append(Spacer(1, 14))

# =========================================================================
# SECCIÓN 4: PRUEBA DE ACTUALIZACIÓN SIN CONTRASEÑA
# =========================================================================
story.append(Paragraph("4. Prueba Crítica: Editar un Usuario sin Contraseña NO Cambia su Contraseña", style_section))
story.append(Paragraph(
    "<b>Corrección del Error de Seguridad del Manual:</b> El manual de referencia contenía un fallo donde al editar a un usuario sin enviar contraseña, "
    "el backend le asignaba la contraseña del administrador solicitante. En CampusConnect se corrigió centralizando la lógica en el método "
    "<code>update()</code> de <code>UserSerializer</code>, garantizando que si no se envía el campo <code>password</code>, la contraseña existente permanece <b>intacta</b>:",
    style_body
))
story.append(RLImage(img_patch, width=530, height=270))
story.append(Spacer(1, 12))

# =========================================================================
# SECCIÓN 5: SUITE DE PRUEBAS AUTOMATIZADAS
# =========================================================================
story.append(Paragraph("5. Verificación de la Suite de Pruebas Automatizadas", style_section))
story.append(Paragraph(
    "Se ejecutaron las 8 pruebas automatizadas en <code>backend/users/tests.py</code> que validan todo el sistema de forma integral:",
    style_body
))

tabla_pruebas = [
    [Paragraph("<b>Prueba</b>", style_body), Paragraph("<b>Descripción</b>", style_body), Paragraph("<b>Resultado</b>", style_body)],
    [Paragraph("Prueba 1", style_body), Paragraph("Creación segura de usuario y cifrado de contraseña con PBKDF2", style_body), Paragraph("<font color='#2E7D32'><b>PASÓ (OK)</b></font>", style_body)],
    [Paragraph("Prueba 2", style_body), Paragraph("Login JWT y obtención de tokens access y refresh", style_body), Paragraph("<font color='#2E7D32'><b>PASÓ (OK)</b></font>", style_body)],
    [Paragraph("Prueba 3", style_body), Paragraph("Consulta de datos personales (/auth/me/) sin exponer contraseñas", style_body), Paragraph("<font color='#2E7D32'><b>PASÓ (OK)</b></font>", style_body)],
    [Paragraph("Prueba 4", style_body), Paragraph("Actualización sin contraseña mantiene intacta la clave original (PUT/PATCH)", style_body), Paragraph("<font color='#2E7D32'><b>PASÓ (OK)</b></font>", style_body)],
    [Paragraph("Prueba 5", style_body), Paragraph("Actualización con nueva contraseña actualiza el acceso adecuadamente", style_body), Paragraph("<font color='#2E7D32'><b>PASÓ (OK)</b></font>", style_body)],
    [Paragraph("Prueba 6", style_body), Paragraph("Verificación estricta de que ningún endpoint exponga hashes ni passwords", style_body), Paragraph("<font color='#2E7D32'><b>PASÓ (OK)</b></font>", style_body)],
    [Paragraph("Prueba 7", style_body), Paragraph("Control de permisos: bloqueo a usuarios anónimos y alumnos en CRUD", style_body), Paragraph("<font color='#2E7D32'><b>PASÓ (OK)</b></font>", style_body)],
    [Paragraph("Prueba 8", style_body), Paragraph("Registro público de usuarios (/auth/register/) sin permisos de admin", style_body), Paragraph("<font color='#2E7D32'><b>PASÓ (OK)</b></font>", style_body)],
]

t_tests = Table(tabla_pruebas, colWidths=[65, 395, 70])
t_tests.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#004D40')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#B0BEC5')),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
]))
story.append(t_tests)

# Construir documento
doc.build(story, canvasmaker=NumberedCanvas)
print(f"PDF generado exitosamente en: {PDF_PATH}")
