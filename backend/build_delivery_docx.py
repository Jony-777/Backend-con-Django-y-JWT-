"""
Generador del documento universitario en formato DOCX:
'Resultado_Aprendizaje_Unidad_2_y_3.docx'
Cumple con toda la estructura académica solicitada e inserta
las 13 capturas de evidencia en sus secciones correspondientes.
"""

import os
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

BASE_DIR = Path(__file__).resolve().parent.parent
EVIDENCIAS_DIR = BASE_DIR / "evidencias"
DOCX_OUTPUT = BASE_DIR / "Resultado_Aprendizaje_Unidad_2_y_3.docx"


def set_cell_background(cell, fill_hex):
    """Aplica color de fondo a una celda de tabla en python-docx"""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)


def build_docx():
    doc = Document()

    # Configuración de márgenes estándar (2.5 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # -------------------------------------------------------------
    # 1. PORTADA ACADÉMICA
    # -------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("ENTREGA UNIVERSITARIA DE INGENIERÍA EN SOFTWARE\n")
    r_inst.font.name = "Calibri"
    r_inst.font.size = Pt(14)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(0, 105, 92)

    r_sub = p_inst.add_run("Desarrollo Web Full Stack – Unidades 2 y 3\n\n\n")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = RGBColor(84, 110, 122)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("Resultado de Aprendizaje Unidad 2 y 3:\nDjango + React con Autenticación y APIs")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0, 77, 64)

    p_space = doc.add_paragraph("\n\n")

    # Tabla de datos en portada
    table_meta = doc.add_table(rows=5, cols=2)
    table_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_info = [
        ("Proyecto:", "CampusTrack (Plataforma Escolar Full Stack)"),
        ("Tecnologías:", "Django 5.1, DRF, SimpleJWT, React 18, Vite, SASS"),
        ("Repositorio GitHub:", "https://github.com/Jony-777/Backend-con-Django-y-JWT-"),
        ("Base de Datos:", "SQLite (excluida de Git)"),
        ("Fecha de Entrega:", "Noviembre 2026"),
    ]
    for i, (k, v) in enumerate(meta_info):
        r_k = table_meta.rows[i].cells[0].paragraphs[0].add_run(k)
        r_k.bold = True
        r_k.font.color.rgb = RGBColor(0, 77, 64)
        r_v = table_meta.rows[i].cells[1].paragraphs[0].add_run(v)
        set_cell_background(table_meta.rows[i].cells[0], "ECEFF1")
        set_cell_background(table_meta.rows[i].cells[1], "FAFAFA")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 2. INTRODUCCIÓN Y OBJETIVO
    # -------------------------------------------------------------
    h1 = doc.add_heading("1. Introducción", level=1)
    h1.runs[0].font.color.rgb = RGBColor(0, 105, 92)

    doc.add_paragraph(
        "En el desarrollo contemporáneo de aplicaciones web empresariales y escolares, la arquitectura orientada a servicios "
        "y el desacoplamiento entre el backend y el frontend constituyen el estándar fundamental de la industria. "
        "Este informe documenta la implementación completa del proyecto CampusTrack, un sistema de administración escolar "
        "cuyo núcleo combina la robustez y seguridad de Django REST Framework en el backend, con la agilidad y experiencia "
        "interactiva de React y Vite en el frontend."
    )
    doc.add_paragraph(
        "El proyecto resuelve dos necesidades esenciales: la gestión centralizada y segura de cuentas de usuario mediante "
        "tokens criptográficos JWT (JSON Web Tokens) y la construcción de una interfaz de usuario fluida, reactiva y protegida."
    )

    h1_obj = doc.add_heading("2. Objetivo de la Práctica", level=1)
    h1_obj.runs[0].font.color.rgb = RGBColor(0, 105, 92)

    doc.add_paragraph(
        "Diseñar, implementar y documentar una plataforma escolar integral con arquitectura desacoplada, cumpliendo los siguientes hitos:"
    )
    p_obj_list = doc.add_paragraph()
    p_obj_list.add_run("• Desarrollar una API RESTful en Django con modelo de usuario personalizado (email como identificador y matrícula).\n")
    p_obj_list.add_run("• Implementar autenticación segura basada en tokens JWT con tiempos de vida controlados (access y refresh).\n")
    p_obj_list.add_run("• Subsanar vulnerabilidades críticas identificadas en el manual respecto al manejo y almacenamiento de contraseñas.\n")
    p_obj_list.add_run("• Crear una aplicación frontend con React y Vite utilizando componentes visuales de Semantic UI y hojas de estilo SASS.\n")
    p_obj_list.add_run("• Establecer la comunicación segura entre cliente y servidor mediante CORS, Context API, Hooks personalizados y Formik con Yup.\n")
    p_obj_list.add_run("• Garantizar la protección de rutas administrativas y la persistencia de sesión sin almacenamiento inseguro de credenciales.")

    # -------------------------------------------------------------
    # 3. TECNOLOGÍAS UTILIZADAS
    # -------------------------------------------------------------
    h1_tec = doc.add_heading("3. Tecnologías Utilizadas", level=1)
    h1_tec.runs[0].font.color.rgb = RGBColor(0, 105, 92)

    table_tec = doc.add_table(rows=9, cols=3)
    table_tec.alignment = WD_TABLE_ALIGNMENT.CENTER
    tec_data = [
        ("Capa", "Tecnología / Biblioteca", "Propósito en el Proyecto"),
        ("Backend", "Python 3.13 + Django 5.1", "Framework backend principal y arquitectura de modelos."),
        ("Backend", "Django REST Framework 3.17", "Construcción de la API RESTful, serializadores y ViewSets."),
        ("Backend", "SimpleJWT 5.5", "Generación, verificación y renovación de tokens Bearer JWT."),
        ("Backend", "drf-yasg 1.21", "Generación de documentación interactiva OpenAPI 2.0 / Swagger UI."),
        ("Backend", "django-cors-headers 4.9", "Habilitación y control de Cross-Origin Resource Sharing."),
        ("Frontend", "React 18 + Vite", "Librería de interfaces y entorno de desarrollo/empaquetado rápido."),
        ("Frontend", "React Router DOM v7", "Sistema modular de enrutamiento y layouts de protección."),
        ("Frontend", "Semantic UI React + SASS", "Diseño responsivo, componentes de formulario y estilos visuales."),
    ]
    for row_idx, data_row in enumerate(tec_data):
        row = table_tec.rows[row_idx]
        for col_idx, val in enumerate(data_row):
            p = row.cells[col_idx].paragraphs[0]
            r = p.add_run(val)
            if row_idx == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
                set_cell_background(row.cells[col_idx], "004D40")
            else:
                if col_idx == 0: r.bold = True
                set_cell_background(row.cells[col_idx], "F5F5F5" if row_idx % 2 == 0 else "FFFFFF")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 4. DESARROLLO DE LA IMPLEMENTACIÓN
    # -------------------------------------------------------------
    h1_dev = doc.add_heading("4. Desarrollo de la Implementación", level=1)
    h1_dev.runs[0].font.color.rgb = RGBColor(0, 105, 92)

    doc.add_paragraph(
        "El proyecto se organizó bajo una estructura limpia que separa nítidamente las responsabilidades del backend y el frontend. "
        "A continuación se presenta la distribución general de directorios:"
    )

    # CAPTURA 1
    doc.add_heading("4.1 Estructura del Proyecto en el Entorno de Desarrollo", level=2)
    doc.add_paragraph(
        "La estructura modular del proyecto incluye el backend en Django con sus aplicaciones y comandos de gestión, "
        "el frontend con su árbol de rutas, contextos, layouts y componentes, y los archivos de configuración de versiones:"
    )
    doc.add_picture(str(EVIDENCIAS_DIR / "01_estructura_proyecto.png"), width=Inches(6.2))
    p_cap1 = doc.add_paragraph("Figura 1: Estructura general de carpetas y archivos en Visual Studio Code.")
    p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap1.runs[0].font.italic = True
    p_cap1.runs[0].font.size = Pt(9)

    # CAPTURA 2
    doc.add_heading("4.2 Ejecución del Servidor Backend (Django)", level=2)
    doc.add_paragraph(
        "El servidor de desarrollo de Django se inicia en el puerto local 8000. Realiza las comprobaciones de sistema "
        "sin advertencias ni errores y atiende las peticiones HTTP provenientes tanto del cliente de React como de Swagger UI:"
    )
    doc.add_picture(str(EVIDENCIAS_DIR / "02_backend_ejecucion.png"), width=Inches(6.2))
    p_cap2 = doc.add_paragraph("Figura 2: Consola del backend Django ejecutándose en http://127.0.0.1:8000/.")
    p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap2.runs[0].font.italic = True
    p_cap2.runs[0].font.size = Pt(9)

    doc.add_page_break()

    # CAPTURA 3
    doc.add_heading("4.3 Documentación de la API mediante Swagger UI", level=2)
    doc.add_paragraph(
        "Mediante la biblioteca drf-yasg se expone la documentación interactiva en /swagger/. Permite examinar los contratos "
        "de cada endpoint, los esquemas de entrada y salida de datos, y autenticar llamadas mediante el botón 'Authorize':"
    )
    doc.add_picture(str(EVIDENCIAS_DIR / "03_swagger_documentacion.png"), width=Inches(6.2))
    p_cap3 = doc.add_paragraph("Figura 3: Catálogo interactivo de endpoints en Swagger UI (/swagger/).")
    p_cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap3.runs[0].font.italic = True
    p_cap3.runs[0].font.size = Pt(9)

    # CAPTURA 4
    doc.add_heading("4.4 Frontend en Funcionamiento (Página Principal)", level=2)
    doc.add_paragraph(
        "El cliente web se desarrolló sobre React 18 impulsado por Vite en http://localhost:5173/. "
        "Ofrece una barra de navegación institucional superior y enlaces directos a las funciones de acceso escolar:"
    )
    doc.add_picture(str(EVIDENCIAS_DIR / "04_frontend_funcionamiento.png"), width=Inches(6.2))
    p_cap4 = doc.add_paragraph("Figura 4: Página principal (Home) de CampusTrack en React.")
    p_cap4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap4.runs[0].font.italic = True
    p_cap4.runs[0].font.size = Pt(9)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 5. AUTENTICACIÓN, LOGIN Y REGISTRO
    # -------------------------------------------------------------
    h1_auth = doc.add_heading("5. Sistema de Autenticación y Control de Acceso", level=1)
    h1_auth.runs[0].font.color.rgb = RGBColor(0, 105, 92)

    doc.add_paragraph(
        "La autenticación se implementó siguiendo el estándar JSON Web Token (JWT). El usuario remite sus credenciales "
        "(correo y contraseña) al endpoint /api/v1/auth/token/. Si son correctas, el backend devuelve un par de tokens:"
    )
    doc.add_paragraph(
        "1. Access Token: Token de corta duración (30 minutos) que se adjunta en la cabecera 'Authorization: Bearer <token>' "
        "para consultar recursos protegidos como /api/v1/auth/me/.\n"
        "2. Refresh Token: Token de larga duración (1 día) destinado a renovar el token de acceso sin forzar al usuario a reintroducir su clave."
    )

    # CAPTURA 5
    doc.add_heading("5.1 Formulario de Inicio de Sesión", level=2)
    doc.add_paragraph(
        "La vista Login.jsx utiliza componentes de Semantic UI y es administrada por Formik y Yup, "
        "garantizando validaciones en el cliente antes de emitir la llamada de red:"
    )
    doc.add_picture(str(EVIDENCIAS_DIR / "05_formulario_login.png"), width=Inches(6.2))
    p_cap5 = doc.add_paragraph("Figura 5: Formulario de inicio de sesión con correo y contraseña.")
    p_cap5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap5.runs[0].font.italic = True
    p_cap5.runs[0].font.size = Pt(9)

    # CAPTURA 6
    doc.add_heading("5.2 Validación de Errores en el Formulario de Login", level=2)
    doc.add_paragraph(
        "Yup comprueba que el correo electrónico cumpla con la sintaxis reglamentaria y que ninguno de los campos "
        "permanezca vacío. Si se detectan inconsistencias, se resaltan los campos y se despliega una notificación de error:"
    )
    doc.add_picture(str(EVIDENCIAS_DIR / "06_validacion_errores_login.png"), width=Inches(6.2))
    p_cap6 = doc.add_paragraph("Figura 6: Validación de campos obligatorios y formato de correo con Yup.")
    p_cap6.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap6.runs[0].font.italic = True
    p_cap6.runs[0].font.size = Pt(9)

    doc.add_page_break()

    # CAPTURA 7
    doc.add_heading("5.3 Inicio de Sesión Exitoso", level=2)
    doc.add_paragraph(
        "Al validar credenciales auténticas, loginApi recibe el token, AuthContext actualiza el estado global de la sesión "
        "y el usuario es notificado visualmente mediante React Toastify mientras es redirigido a /dashboard:"
    )
    doc.add_picture(str(EVIDENCIAS_DIR / "07_inicio_sesion_exitoso.png"), width=Inches(6.2))
    p_cap7 = doc.add_paragraph("Figura 7: Inicio de sesión correcto y notificación toast de confirmación.")
    p_cap7.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap7.runs[0].font.italic = True
    p_cap7.runs[0].font.size = Pt(9)

    # CAPTURA 8
    doc.add_heading("5.4 Dashboard Privado con Información del Usuario", level=2)
    doc.add_paragraph(
        "El Dashboard es una ruta protegida envuelta en AdminLayout. Recupera los datos de request.user a través de "
        "GET /api/v1/auth/me/ y despliega el correo, nombre completo, matrícula escolar y rol:"
    )
    doc.add_picture(str(EVIDENCIAS_DIR / "08_dashboard_usuario.png"), width=Inches(6.2))
    p_cap8 = doc.add_paragraph("Figura 8: Dashboard privado mostrando los datos reales del usuario.")
    p_cap8.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap8.runs[0].font.italic = True
    p_cap8.runs[0].font.size = Pt(9)

    doc.add_page_break()

    # CAPTURA 9
    doc.add_heading("5.5 Persistencia de Sesión (Recarga de Página F5)", level=2)
    doc.add_paragraph(
        "Al actualizar la ventana del navegador, el hook useEffect de AuthProvider lee el token en localStorage y consulta "
        "/auth/me/ para verificar su validez. La sesión se mantiene íntegra sin solicitar reautenticación:"
    )
    doc.add_picture(str(EVIDENCIAS_DIR / "09_persistencia_sesion.png"), width=Inches(6.2))
    p_cap9 = doc.add_paragraph("Figura 9: Persistencia del token en localStorage e inspección en Developer Tools.")
    p_cap9.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap9.runs[0].font.italic = True
    p_cap9.runs[0].font.size = Pt(9)

    # CAPTURA 10
    doc.add_heading("5.6 Cierre de Sesión Seguro", level=2)
    doc.add_paragraph(
        "Al pulsar 'Cerrar Sesión', se ejecuta removeToken() en localStorage, se limpia el contexto global y el usuario "
        "es expulsado del Dashboard hacia la pantalla de login, perdiendo acceso a las rutas protegidas:"
    )
    doc.add_picture(str(EVIDENCIAS_DIR / "10_cierre_sesion.png"), width=Inches(6.2))
    p_cap10 = doc.add_paragraph("Figura 10: Limpieza de credenciales en almacenamiento local y redirección a login.")
    p_cap10.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap10.runs[0].font.italic = True
    p_cap10.runs[0].font.size = Pt(9)

    doc.add_page_break()

    # CAPTURA 11
    doc.add_heading("5.7 Formulario de Registro Escolar", level=2)
    doc.add_paragraph(
        "La vista Register.jsx proporciona un formulario público conectado al endpoint /api/v1/auth/register/. "
        "Solicita nombre, apellido, correo electrónico, matrícula opcional y contraseña con un mínimo de 6 caracteres:"
    )
    doc.add_picture(str(EVIDENCIAS_DIR / "11_formulario_registro.png"), width=Inches(6.2))
    p_cap11 = doc.add_paragraph("Figura 11: Formulario de creación de cuenta escolar para nuevos alumnos.")
    p_cap11.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap11.runs[0].font.italic = True
    p_cap11.runs[0].font.size = Pt(9)

    # CAPTURA 12
    doc.add_heading("5.8 Confirmación de Registro Exitoso", level=2)
    doc.add_paragraph(
        "Al completar el registro, el backend cifra la contraseña mediante PBKDF2/SHA256, crea el registro escolar "
        "con privilegios regulares (is_staff=False) y el frontend despliega la confirmación de éxito:"
    )
    doc.add_picture(str(EVIDENCIAS_DIR / "12_registro_exitoso.png"), width=Inches(6.2))
    p_cap12 = doc.add_paragraph("Figura 12: Registro satisfactorio de una nueva alumna escolar (Valeria Sánchez).")
    p_cap12.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap12.runs[0].font.italic = True
    p_cap12.runs[0].font.size = Pt(9)

    doc.add_page_break()

    # CAPTURA 13
    doc.add_heading("5.9 Verificación del Registro en Django Admin", level=2)
    doc.add_paragraph(
        "Al consultar el panel administrativo de Django (/admin/users/user/), el nuevo usuario registrado se visualiza "
        "correctamente incorporado en la base de datos con su correo, nombre, matrícula y roles:"
    )
    doc.add_picture(str(EVIDENCIAS_DIR / "13_usuario_django_admin.png"), width=Inches(6.2))
    p_cap13 = doc.add_paragraph("Figura 13: Panel de Django Admin con los usuarios registrados y sus estados.")
    p_cap13.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap13.runs[0].font.italic = True
    p_cap13.runs[0].font.size = Pt(9)

    # -------------------------------------------------------------
    # 6. CORRECCIONES DE SEGURIDAD Y PRUEBAS
    # -------------------------------------------------------------
    h1_sec = doc.add_heading("6. Correcciones Críticas de Seguridad Realizadas", level=1)
    h1_sec.runs[0].font.color.rgb = RGBColor(0, 105, 92)

    doc.add_paragraph(
        "Durante el desarrollo se subsanaron dos vulnerabilidades de seguridad críticas presentes en el manual de referencia:"
    )
    p_sec1 = doc.add_paragraph()
    p_sec1.add_run("1. Cifrado obligatorio en creación (create): ").bold = True
    p_sec1.add_run("El campo password se configuró como write_only=True en UserSerializer y RegisterSerializer. "
                   "La clave se procesa con set_password() utilizando PBKDF2/SHA256 y nunca se retorna en las respuestas JSON.")

    p_sec2 = doc.add_paragraph()
    p_sec2.add_run("2. Solución a la sobreescritura de contraseñas en edición (update / partial_update): ").bold = True
    p_sec2.add_run("El manual original contenía un fallo severo: cuando no se enviaba el campo password en una actualización, "
                   "se asignaba request.user.password, provocando que la cuenta del usuario editado terminara con la clave del administrador. "
                   "En CampusTrack se corrigió extrayendo la contraseña mediante validated_data.pop('password', None): "
                   "si no se envía, la contraseña previa permanece intacta y jamás se vincula a la del administrador solicitante.")

    # -------------------------------------------------------------
    # 7. CONCLUSIÓN
    # -------------------------------------------------------------
    h1_concl = doc.add_heading("7. Conclusiones", level=1)
    h1_concl.runs[0].font.color.rgb = RGBColor(0, 105, 92)

    doc.add_paragraph(
        "La integración entre Django REST Framework y React con Vite permitió consolidar una arquitectura web "
        "altamente escalable, desacoplada y eficiente. La gestión de estados mediante Context API y React Router DOM "
        "hizo posible proteger de manera efectiva las rutas de administración, garantizando que el acceso a datos sensibles "
        "requiera obligatoriamente un token JWT válido."
    )
    doc.add_paragraph(
        "Asimismo, la identificación y corrección de las vulnerabilidades del manual en el manejo de contraseñas reafirma la "
        "importancia de no asumir como infalibles los ejemplos introductorios, aplicando principios de defensa en profundidad, "
        "cifrado criptográfico unidireccional y aislamiento estricto entre identidades de usuario."
    )

    doc.save(str(DOCX_OUTPUT))
    print(f"Documento DOCX generado exitosamente en: {DOCX_OUTPUT}")


if __name__ == "__main__":
    build_docx()
