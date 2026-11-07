"""
Generador del documento universitario en formato PDF:
'Resultado_Aprendizaje_Unidad_2_y_3.pdf'
Exportación equivalente del DOCX con ReportLab.
"""

import os
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

BASE_DIR = Path(__file__).resolve().parent.parent
EVIDENCIAS_DIR = BASE_DIR / "evidencias"
PDF_OUTPUT = BASE_DIR / "Resultado_Aprendizaje_Unidad_2_y_3.pdf"


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
        self.setStrokeColor(colors.HexColor("#CFD8DC"))
        self.setLineWidth(0.5)
        self.line(40, 40, letter[0] - 40, 40)
        self.drawString(40, 26, "Resultado de Aprendizaje Unidad 2 y 3: Django + React con Autenticación y APIs")
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(letter[0] - 40, 26, page_text)
        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        str(PDF_OUTPUT),
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=55
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#004D40'),
        alignment=1,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#00695C'),
        spaceBefore=12,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#004D40'),
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#263238'),
        spaceAfter=6
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Italic'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#546E7A'),
        alignment=1,
        spaceBefore=3,
        spaceAfter=10
    )

    story = []

    # Portada
    story.append(Paragraph("UNIVERSIDAD TECNOLÓGICA / FACULTAD DE INFORMÁTICA", ParagraphStyle('Inst', parent=body_style, fontName='Helvetica-Bold', alignment=1, textColor=colors.HexColor('#00695C'))))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Resultado de Aprendizaje Unidad 2 y 3:<br/>Django + React con Autenticación y APIs", title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#00897B"), spaceAfter=15))

    meta = [
        [Paragraph("<b>Proyecto:</b>", body_style), Paragraph("CampusTrack (Plataforma Escolar Full Stack)", body_style)],
        [Paragraph("<b>Tecnologías:</b>", body_style), Paragraph("Django 5.1, DRF, JWT, React 18, Vite, SASS", body_style)],
        [Paragraph("<b>Repositorio GitHub:</b>", body_style), Paragraph('<a href="https://github.com/Jony-777/Backend-con-Django-y-JWT-"><u>https://github.com/Jony-777/Backend-con-Django-y-JWT-</u></a>', body_style)],
        [Paragraph("<b>Base de Datos:</b>", body_style), Paragraph("SQLite (excluida del repositorio)", body_style)],
        [Paragraph("<b>Evaluación:</b>", body_style), Paragraph("Unidad 2 (Backend APIs) y Unidad 3 (Frontend React + JWT)", body_style)]
    ]
    t_meta = Table(meta, colWidths=[130, 400])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#ECEFF1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CFD8DC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#B0BEC5')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 20))

    # Introducción
    story.append(Paragraph("1. Introducción y Objetivo de la Práctica", h1_style))
    story.append(Paragraph(
        "El presente proyecto integra una solución web desacoplada para la gestión de usuarios escolares denominada CampusTrack. "
        "En el backend se empleó Django y Django REST Framework para proveer servicios RESTful protegidos por tokens JWT (JSON Web Tokens). "
        "En el frontend se implementó una interfaz reactiva mediante React y Vite con estilos personalizados en SASS y componentes Semantic UI.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Objetivo:</b> Diseñar una arquitectura segura que subsane vulnerabilidades críticas del manual en el almacenamiento y edición "
        "de contraseñas, asegurando que ninguna clave se guarde en texto plano ni se sobreescriba indebidamente, conectando de forma "
        "íntegra el ciclo de registro, inicio de sesión, persistencia de estado y cierre de sesión.",
        body_style
    ))

    # Desarrollo y Capturas
    story.append(Paragraph("2. Desarrollo de la Implementación y Evidencias", h1_style))

    caps = [
        ("01_estructura_proyecto.png", "Figura 1: Estructura general de carpetas y archivos en el editor Visual Studio Code.", "2.1 Estructura del Proyecto"),
        ("02_backend_ejecucion.png", "Figura 2: Consola del backend Django ejecutándose en http://127.0.0.1:8000/.", "2.2 Servidor Backend Django en Ejecución"),
        ("03_swagger_documentacion.png", "Figura 3: Documentación interactiva de endpoints mediante Swagger UI (/swagger/).", "2.3 Documentación de la API en Swagger UI"),
        ("04_frontend_funcionamiento.png", "Figura 4: Frontend CampusTrack en funcionamiento en http://localhost:5173/.", "2.4 Frontend React en Funcionamiento"),
        ("05_formulario_login.png", "Figura 5: Formulario de inicio de sesión con correo y contraseña.", "2.5 Formulario de Inicio de Sesión"),
        ("06_validacion_errores_login.png", "Figura 6: Validación de campos obligatorios y formato de correo con Formik y Yup.", "2.6 Validación de Errores en Login"),
        ("07_inicio_sesion_exitoso.png", "Figura 7: Inicio de sesión exitoso y confirmación con notificación Toastify.", "2.7 Inicio de Sesión Exitoso"),
        ("08_dashboard_usuario.png", "Figura 8: Dashboard privado mostrando datos reales del usuario autenticado.", "2.8 Dashboard con Datos del Usuario"),
        ("09_persistencia_sesion.png", "Figura 9: Persistencia de sesión tras recargar el navegador (token en localStorage).", "2.9 Persistencia de Sesión (F5 / Reload)"),
        ("10_cierre_sesion.png", "Figura 10: Cierre de sesión, eliminación de token y redirección segura al login.", "2.10 Cierre de Sesión Seguro"),
        ("11_formulario_registro.png", "Figura 11: Formulario de creación de cuenta escolar para nuevos alumnos.", "2.11 Formulario de Registro Escolar"),
        ("12_registro_exitoso.png", "Figura 12: Registro exitoso de nueva usuaria escolar (Valeria Sánchez).", "2.12 Registro Exitoso de Alumno"),
        ("13_usuario_django_admin.png", "Figura 13: Panel de Django Admin con los usuarios registrados en el sistema.", "2.13 Usuarios Registrados en Django Admin"),
    ]

    for img_name, caption, subtitle in caps:
        img_p = EVIDENCIAS_DIR / img_name
        if img_p.exists():
            story.append(Paragraph(subtitle, h2_style))
            story.append(RLImage(str(img_p), width=530, height=260))
            story.append(Paragraph(caption, caption_style))

    # Conclusión
    story.append(Paragraph("3. Conclusiones y Correcciones de Seguridad", h1_style))
    story.append(Paragraph(
        "• <b>Cifrado estricto de contraseñas:</b> El campo <code>password</code> está configurado como <code>write_only=True</code>. "
        "Las claves se procesan con <code>set_password()</code> mediante PBKDF2/SHA256, sin exponer hashes en las respuestas.<br/>"
        "• <b>Corrección del error del manual en edición:</b> Al actualizar usuarios mediante PUT o PATCH, si no se envía una nueva contraseña, "
        "la contraseña original se conserva intacta y nunca se sobreescribe con la del administrador.<br/>"
        "• <b>Integración React + JWT:</b> La combinación de React Router DOM, AuthContext y localStorage asegura la protección de rutas "
        "y la persistencia transparente de la sesión.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Documento PDF generado exitosamente en: {PDF_OUTPUT}")


if __name__ == "__main__":
    build_pdf()
