// src/routes/routes.common.jsx
// Rutas comunes: login, registro y página de error 404.

import { CommonLayout } from '../layouts/CommonLayout';
import { Login, Register, Error404 } from '../pages/common';

export const routesCommon = [
  {
    path: '/login',
    layout: CommonLayout,
    component: Login,
  },
  {
    path: '/register',
    layout: CommonLayout,
    component: Register,
  },
  {
    path: '*',
    layout: CommonLayout,
    component: Error404,
  },
];

