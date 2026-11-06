// src/api/user.js
// Funciones para comunicarse con la API de CampusConnect en Django.

const BASE_URL = import.meta.env.VITE_BASE_API_URL || 'http://localhost:8000';

/**
 * Inicia sesión con email y contraseña.
 * POST /api/v1/auth/token/
 * @param {string} email
 * @param {string} password
 * @returns {Promise<{access: string, refresh: string}>}
 */
export async function loginApi(email, password) {
  const response = await fetch(`${BASE_URL}/api/v1/auth/token/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || 'Credenciales incorrectas. Verifica tu correo y contraseña.');
  }
  return data;
}

/**
 * Obtiene los datos del usuario autenticado.
 * GET /api/v1/auth/me/
 * @param {string} token - Bearer access token
 * @returns {Promise<{id, email, first_name, last_name, matricula, is_active}>}
 */
export async function getMeApi(token) {
  const response = await fetch(`${BASE_URL}/api/v1/auth/me/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || 'No se pudieron obtener los datos del usuario.');
  }
  return data;
}

/**
 * Registra un nuevo usuario sin necesidad de autenticación.
 * POST /api/v1/auth/register/
 * @param {object} userData - { email, password, first_name, last_name, matricula }
 * @returns {Promise<{message: string, user: object}>}
 */
export async function registerApi(userData) {
  const response = await fetch(`${BASE_URL}/api/v1/auth/register/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData),
  });
  const data = await response.json();
  if (!response.ok) {
    // Extrae el primer mensaje de error de Django REST Framework
    const firstError = Object.values(data)[0];
    const message = Array.isArray(firstError) ? firstError[0] : firstError;
    throw new Error(message || 'Error al registrar el usuario. Intenta de nuevo.');
  }
  return data;
}

