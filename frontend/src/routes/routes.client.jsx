// src/routes/routes.client.jsx
// Rutas de la zona pública del cliente (visitantes autenticados o no).

import { ClientLayout } from '../layouts/ClientLayout';
import { Home } from '../pages/client';

export const routesClient = [
  {
    path: '/',
    layout: ClientLayout,
    component: Home,
  },
  {
    path: '/home',
    layout: ClientLayout,
    component: Home,
  },
];

