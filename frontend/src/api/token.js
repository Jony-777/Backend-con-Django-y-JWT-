// src/api/token.js
// Gestión segura del token JWT en localStorage.
// IMPORTANTE: Nunca se almacena la contraseña, solo el token de acceso.

const TOKEN_KEY = import.meta.env.VITE_LOCAL_STORAGE_ITEM_NAME || 'TOKEN';

/**
 * Guarda el token JWT en localStorage.
 * @param {string} token - El access token recibido del backend.
 */
export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

/**
 * Recupera el token JWT guardado en localStorage.
 * @returns {string|null} El token guardado, o null si no existe.
 */
export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

/**
 * Elimina el token JWT de localStorage.
 * Se debe llamar al cerrar sesión.
 */
export function removeToken() {
  localStorage.removeItem(TOKEN_KEY);
}

