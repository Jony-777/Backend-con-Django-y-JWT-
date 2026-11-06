// src/routes/Navigation.jsx
// Componente principal de navegación. Renderiza las rutas envolviéndolas en su Layout.

import { Route, Routes } from 'react-router-dom';
import { routes } from './routes';

export function Navigation() {
  return (
    <Routes>
      {routes.map((route) => {
        const { path, layout: Layout, component: Component } = route;
        return (
          <Route
            key={path}
            path={path}
            element={
              <Layout>
                <Component />
              </Layout>
            }
          />
        );
      })}
    </Routes>
  );
}

