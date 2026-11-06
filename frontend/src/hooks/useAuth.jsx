// src/hooks/useAuth.jsx
// Hook personalizado para consumir el contexto de autenticación.
// Usar este hook en lugar de useContext(AuthContext) directamente.

import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

/**
 * Hook que devuelve el estado y las acciones de autenticación.
 * @returns {{ user, token, isAuthenticated, isLoading, login, logout }}
 */
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe usarse dentro de un AuthProvider.');
  }
  return context;
}

