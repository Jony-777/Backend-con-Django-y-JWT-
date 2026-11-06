// src/hooks/useUser.jsx
// Hook personalizado para consultar los datos del usuario autenticado.

import { useState, useCallback } from 'react';
import { getMeApi } from '../api/user';
import { useAuth } from './useAuth';

/**
 * Hook que permite recuperar los datos del usuario autenticado
 * llamando al endpoint GET /api/v1/auth/me/.
 * Útil para refrescar los datos del perfil sin recargar la página.
 */
export function useUser() {
  const { token } = useAuth();
  const [userData, setUserData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchUser = useCallback(async () => {
    if (!token) return;
    setIsLoading(true);
    setError(null);
    try {
      const data = await getMeApi(token);
      setUserData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }, [token]);

  return { userData, isLoading, error, fetchUser };
}

