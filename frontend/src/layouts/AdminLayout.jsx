// src/layouts/AdminLayout.jsx
// Layout para las páginas del área administrativa (ej. Dashboard).
// Protege el acceso: si el usuario no está autenticado, redirige al login.

import { Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export function AdminLayout({ children }) {
  const { isAuthenticated, isLoading } = useAuth();

  // Mientras se verifica la sesión (carga inicial), no renderizamos nada
  // para evitar un parpadeo o redirección prematura.
  if (isLoading) {
    return null;
  }

  // Si el usuario no está autenticado, lo redirigimos a la página de login.
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <div className="admin-layout">{children}</div>;
}

