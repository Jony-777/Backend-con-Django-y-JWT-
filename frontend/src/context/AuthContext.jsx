// src/context/AuthContext.jsx
// Contexto global de autenticación para CampusConnect.
// Comparte el estado de sesión entre todos los componentes de la aplicación.

import { createContext, useState, useEffect, useCallback } from 'react';
import { getToken, setToken, removeToken } from '../api/token';
import { getMeApi } from '../api/user';

// Creamos el contexto exportable para ser consumido mediante useAuth
export const AuthContext = createContext({
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: true,
  login: async () => {},
  logout: () => {},
});

/**
 * AuthProvider: envuelve la aplicación y proporciona el estado de autenticación.
 * Al cargar la aplicación, verifica si existe un token válido en localStorage.
 */
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setTokenState] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Al montar el componente, intenta restaurar la sesión desde el token guardado
  useEffect(() => {
    const restoreSession = async () => {
      const savedToken = getToken();
      if (!savedToken) {
        setIsLoading(false);
        return;
      }
      try {
        const userData = await getMeApi(savedToken);
        setUser(userData);
        setTokenState(savedToken);
      } catch {
        // El token puede haber expirado. Limpiamos el estado sin mostrar error al usuario.
        removeToken();
        setUser(null);
        setTokenState(null);
      } finally {
        setIsLoading(false);
      }
    };

    restoreSession();
  }, []);

  /**
   * Inicia sesión: guarda el token y recupera los datos del usuario.
   * @param {string} accessToken - Token JWT recibido del endpoint /auth/token/
   */
  const login = useCallback(async (accessToken) => {
    setToken(accessToken);
    setTokenState(accessToken);
    const userData = await getMeApi(accessToken);
    setUser(userData);
  }, []);

  /**
   * Cierra sesión: elimina el token y limpia el estado de autenticación.
   */
  const logout = useCallback(() => {
    removeToken();
    setUser(null);
    setTokenState(null);
  }, []);

  const value = {
    user,
    token,
    isAuthenticated: !!user,
    isLoading,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

