# CampusConnect - Sistema Escolar Full Stack (Django + React)

Plataforma web integral para la administración de usuarios escolares desarrollada con **Django** + **Django REST Framework** en el backend y **React** + **Vite** en el frontend.

Proyecto desarrollado con base en el manual *"Desarrollo Full Stack con Django y ReactJS"* (páginas 5 a 35), incorporando todas las buenas prácticas de seguridad, arquitectura por capas y diseño responsivo.

---

## 📌 Tabla de Contenidos

- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación y Configuración](#-instalación-y-configuración)
  - [Backend (Django)](#backend-django)
  - [Frontend (React + Vite)](#frontend-react--vite)
- [Ejecución del Proyecto](#-ejecución-del-proyecto)
- [Direcciones y URLs del Sistema](#-direcciones-y-urls-del-sistema)
- [Arquitectura del Frontend](#-arquitectura-del-frontend)
- [Endpoints del Backend (API v1)](#-endpoints-del-backend-api-v1)
- [Medidas de Seguridad y Correcciones del Manual](#-medidas-de-seguridad-y-correcciones-del-manual)
- [Pruebas Automatizadas](#-pruebas-automatizadas)
- [Subida a GitHub](#-subida-a-github)

---

## 🚀 Tecnologías Utilizadas

### Backend
- **Python 3.10+** (probado en 3.13)
- **Django 5.1.x**
- **Django REST Framework (DRF) 3.17.x**
- **django-cors-headers 4.9.x** (CORS para comunicación con Vite)
- **djangorestframework-simplejwt 5.5.x** (Autenticación JWT Bearer)
- **drf-yasg 1.21.x** (Swagger UI y ReDoc interactivos)
- **SQLite** como base de datos local

### Frontend
- **JavaScript (ES6+)**
- **React 18.x** con **Vite**
- **React Router DOM v7** (sistema modular de rutas y layouts)
- **Semantic UI React & Semantic UI CSS** (componentes visuales)
- **SASS** (`App.scss` para estilos globales y temas)
- **Formik** + **Yup** (gestión y validación estricta de formularios)
- **React Toastify** (notificaciones toast en `bottom-center`)

---

## 📂 Estructura del Proyecto

```text
CampusConnect/
│
├── backend/
│   ├── campusconnect/                       # Configuración Django
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py                      # CORS, JWT, Apps y Base de Datos
│   │   ├── urls.py                          # Rutas maestras (/admin/, /api/v1/, /swagger/, /redoc/)
│   │   └── wsgi.py
│   │
│   ├── users/                               # Aplicación de gestión de usuarios
│   │   ├── management/commands/
│   │   │   └── seed_data.py                 # Comando para generar usuarios de prueba
│   │   ├── migrations/
│   │   ├── admin.py                         # Panel de administración seguro
│   │   ├── forms.py                         # Formularios de creación/edición en Admin
│   │   ├── models.py                        # Modelo User con email identificador y matrícula
│   │   ├── serializers.py                   # UserSerializer, RegisterSerializer, UserMeSerializer
│   │   ├── tests.py                         # Suite con las 8 pruebas automatizadas
│   │   ├── urls.py                          # Enrutamiento /auth/ y ViewSet /users/
│   │   └── views.py                         # Login JWT, RegisterView, UserMeView, UserViewSet
│   │
│   ├── manage.py
│   ├── requirements.txt                     # Dependencias backend fijadas
│   ├── .gitignore
│   └── db.sqlite3                           # Base de datos SQLite
│
├── frontend/                                # Cliente web React + Vite (JavaScript)
│   ├── src/
│   │   ├── api/                             # Comunicación con la API de Django
│   │   │   ├── token.js                     # setToken, getToken, removeToken en localStorage
│   │   │   └── user.js                      # loginApi, getMeApi, registerApi
│   │   ├── context/
│   │   │   └── AuthContext.jsx              # Contexto global y proveedor de autenticación
│   │   ├── hooks/                           # Custom Hooks
│   │   │   ├── useAuth.jsx                  # Acceso al contexto de autenticación
│   │   │   └── useUser.jsx                  # Hook para consultar perfil (/auth/me/)
│   │   ├── layouts/                         # Layouts por zona
│   │   │   ├── AdminLayout.jsx              # Protege rutas privadas (redirige a /login)
│   │   │   ├── ClientLayout.jsx             # Layout para la zona pública (Home)
│   │   │   ├── CommonLayout.jsx             # Layout para Login, Register y 404
│   │   │   └── index.jsx
│   │   ├── pages/                           # Páginas y vistas
│   │   │   ├── admin/
│   │   │   │   ├── Dashboard.jsx            # Panel privado con correo y botón Cerrar Sesión
│   │   │   │   └── index.jsx
│   │   │   ├── client/
│   │   │   │   ├── Home.jsx                 # Página de bienvenida pública
│   │   │   │   └── index.jsx
│   │   │   └── common/
│   │   │       ├── Login.jsx                # Formulario de inicio de sesión con Formik y Yup
│   │   │       ├── Register.jsx             # Formulario de registro escolar
│   │   │       ├── Error404.jsx             # Vista para rutas inexistentes
│   │   │       └── index.jsx
│   │   ├── routes/                          # Enrutamiento modular
│   │   │   ├── Navigation.jsx               # Componente <Routes> mapeado con layouts
│   │   │   ├── routes.admin.jsx             # Rutas /dashboard
│   │   │   ├── routes.client.jsx            # Rutas / y /home
│   │   │   ├── routes.common.jsx            # Rutas /login, /register, *
│   │   │   ├── routes.js                    # Fusión de todas las rutas
│   │   │   └── index.jsx
│   │   ├── App.jsx                          # Configura BrowserRouter, AuthProvider, ToastContainer
│   │   ├── App.scss                         # Estilos personalizados y variables SASS
│   │   └── main.jsx                         # Entrada de React y montaje en DOM
│   │
│   ├── .env                                 # Variables: VITE_BASE_API_URL y VITE_LOCAL_STORAGE_ITEM_NAME
│   ├── index.html                           # Plantilla HTML con contenedor #root
│   ├── package.json                         # Dependencias y scripts de Vite
│   ├── vite.config.js                       # Configuración de Vite con plugin React
│   └── .gitignore
│
├── .vscode/                                 # Configuración para depuración en VS Code
│   ├── launch.json
│   └── settings.json
├── .gitignore
└── README.md
```

---

## 📋 Requisitos Previos

1. **Python 3.10 o superior**
2. **Node.js 18 o superior** y **npm**
3. **Git** para control de versiones

---

## ⚙️ Instalación y Configuración

### Backend (Django)

1. Abre una terminal y dirígete a `CampusConnect/backend`:
   ```bash
   cd CampusConnect/backend
   ```

2. Activa el entorno virtual:
   - **En Windows (PowerShell):**
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **En Linux / macOS:**
     ```bash
     source venv/bin/activate
     ```

3. Instala las dependencias (si configuras en un nuevo equipo):
   ```bash
   pip install -r requirements.txt
   ```

4. Aplica las migraciones:
   ```bash
   python manage.py migrate
   ```

5. Genera los usuarios iniciales de prueba (superusuario y alumnos):
   ```bash
   python manage.py seed_data
   ```

   **Usuarios generados automáticamente:**
   - **Administrador:** `admin@campusconnect.edu` / `Admin123456!` (Matrícula: `ADM-001`)
   - **Alumno 1:** `carlos.ramirez@campusconnect.edu` / `Alumno123456!` (Matrícula: `MAT-2026-001`)
   - **Alumno 2:** `ana.torres@campusconnect.edu` / `Alumno123456!` (Matrícula: `MAT-2026-002`)

### Frontend (React + Vite)

1. Abre otra terminal y dirígete a `CampusConnect/frontend`:
   ```bash
   cd CampusConnect/frontend
   ```

2. Instala las dependencias de Node:
   ```bash
   npm install
   ```

3. Verifica el archivo `.env` en `frontend/.env`:
   ```env
   VITE_BASE_API_URL=http://localhost:8000
   VITE_LOCAL_STORAGE_ITEM_NAME=TOKEN
   ```

---

## 💻 Ejecución del Proyecto

Para que el sistema funcione completamente, deben estar corriendo ambos servidores simultáneamente:

### Terminal 1: Iniciar el Backend
```bash
cd CampusConnect/backend
.\venv\Scripts\Activate.ps1
python manage.py runserver
```
*Disponible en: `http://localhost:8000/`*

### Terminal 2: Iniciar el Frontend
```bash
cd CampusConnect/frontend
npm run dev
```
*Disponible en: `http://localhost:5173/`*

---

## 🌐 Direcciones y URLs del Sistema

| Servicio / Pantalla | URL | Acceso |
| :--- | :--- | :--- |
| **Frontend - Home** | [http://localhost:5173/](http://localhost:5173/) | Público |
| **Frontend - Login** | [http://localhost:5173/login](http://localhost:5173/login) | Público |
| **Frontend - Registro** | [http://localhost:5173/register](http://localhost:5173/register) | Público |
| **Frontend - Dashboard** | [http://localhost:5173/dashboard](http://localhost:5173/dashboard) | Privado (requiere login) |
| **Backend - Swagger UI** | [http://localhost:8000/swagger/](http://localhost:8000/swagger/) | Documentación interactiva |
| **Backend - ReDoc** | [http://localhost:8000/redoc/](http://localhost:8000/redoc/) | Documentación técnica |
| **Backend - Django Admin** | [http://localhost:8000/admin/](http://localhost:8000/admin/) | Administración Django |

---

## 🎨 Arquitectura del Frontend

1. **Gestión de Rutas (`routes/`)**: Estructura modular dividida en `routes.admin.jsx`, `routes.client.jsx` y `routes.common.jsx`. Mapeadas dinámicamente mediante `Navigation.jsx` envolviendo cada vista con su Layout correspondiente.
2. **Layouts de Protección (`layouts/`)**: `AdminLayout` consume `useAuth`. Si el usuario no tiene una sesión activa, lo redirige automáticamente a `/login` sin parpadeos visuales (`isLoading`).
3. **Formularios con Formik y Yup**:
   - `Login.jsx`: Valida email obligatorio con formato válido y contraseña obligatoria.
   - `Register.jsx`: Valida nombre, apellido, email, contraseña (mínimo 6 caracteres) y matrícula opcional.
4. **Almacenamiento Seguro del Token (`api/token.js`)**: Solo se guarda el token JWT en `localStorage`. **Nunca se guardan contraseñas**.
5. **Persistencia de Sesión (`AuthContext.jsx`)**: Al recargar la página, `useEffect` lee el token en `localStorage` y consulta `getMeApi` para validar que el token siga vigente y restaurar los datos del usuario.

---

## 📡 Endpoints del Backend (API v1)

Prefijo: `/api/v1/`

| Método | Endpoint | Permiso | Descripción |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/token/` | `AllowAny` | Iniciar sesión (recibe `email` y `password`, retorna `access` y `refresh`). |
| `POST` | `/api/v1/auth/token/refresh/` | `AllowAny` | Refrescar token de acceso JWT. |
| `POST` | `/api/v1/auth/register/` | `AllowAny` | Registro público de nuevos usuarios escolares. |
| `GET` | `/api/v1/auth/me/` | `IsAuthenticated` | Consultar perfil del usuario autenticado (sin contraseñas). |
| `GET` | `/api/v1/users/` | `IsAdminUser` | Listar todos los usuarios escolares (CRUD administrativo). |
| `POST` | `/api/v1/users/` | `IsAdminUser` | Crear usuario con contraseña cifrada. |
| `GET` | `/api/v1/users/{id}/` | `IsAdminUser` | Detalle de un usuario específico. |
| `PUT` | `/api/v1/users/{id}/` | `IsAdminUser` | Actualización total (preserva contraseña si no se envía). |
| `PATCH` | `/api/v1/users/{id}/` | `IsAdminUser` | Actualización parcial (preserva contraseña si no se envía). |
| `DELETE` | `/api/v1/users/{id}/` | `IsAdminUser` | Eliminar usuario. |

---

## 🛡️ Medidas de Seguridad y Correcciones del Manual

1. **CORS Configurado**: Se instaló `django-cors-headers` y se especificó `CORS_ALLOWED_ORIGINS` para los puertos de Vite (`5173`, `3000`), evitando peticiones no autorizadas.
2. **Corrección de Registro de Usuarios**: Los datos de registro se obtienen de `request.data` (formulario enviado), **nunca del usuario que realiza la petición**. El registro público siempre asigna `is_staff=False` e `is_superuser=False` para evitar escalada de privilegios.
3. **Cifrado Obligatorio de Contraseñas**: Todas las contraseñas se almacenan mediante `set_password()` con PBKDF2/SHA256. El campo `password` es `write_only=True` y jamás se expone en ninguna respuesta HTTP.
4. **Protección en Actualizaciones**: En PUT y PATCH de usuarios, si no se envía el campo `password`, la contraseña existente **se mantiene intacta** y jamás se asigna la contraseña del administrador.

---

## 🧪 Pruebas Automatizadas

El backend cuenta con una suite completa de 8 pruebas en `backend/users/tests.py`:

```bash
cd CampusConnect/backend
python manage.py test users
```

**Resultado:**
```text
Creating test database for alias 'default'...
Found 8 test(s).
........
----------------------------------------------------------------------
Ran 8 tests in ~40s

OK
Destroying test database for alias 'default'...
```

Para verificar que el frontend compila sin errores:
```bash
cd CampusConnect/frontend
npm run build
```

---

## 📤 Subida a GitHub

El proyecto está configurado para no incluir carpetas pesadas ni archivos sensibles (`backend/venv/`, `backend/db.sqlite3`, `backend/**/__pycache__/`, `frontend/node_modules/`, `frontend/dist/`, `.env`):

```bash
cd CampusConnect
git add .
git commit -m "feat: implementacion full stack de CampusConnect con React, Vite, JWT y registro escolar"
git branch -M main
git push -u origin main
```
