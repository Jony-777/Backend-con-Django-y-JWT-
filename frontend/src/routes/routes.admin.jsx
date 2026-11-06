// src/routes/routes.admin.jsx
// Rutas protegidas del área de administración.

import { AdminLayout } from '../layouts/AdminLayout';
import { Dashboard } from '../pages/admin';

export const routesAdmin = [
  {
    path: '/dashboard',
    layout: AdminLayout,
    component: Dashboard,
  },
];

