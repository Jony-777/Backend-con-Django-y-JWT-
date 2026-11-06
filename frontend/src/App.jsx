// src/App.jsx
// Componente raíz de CampusConnect.
// Configura BrowserRouter, el contexto de autenticación, Toastify y la navegación.

import { BrowserRouter } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'semantic-ui-css/semantic.min.css';
import 'react-toastify/dist/ReactToastify.css';
import './App.scss';

import { AuthProvider } from './context/AuthContext';
import { Navigation } from './routes';

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        {/* Sistema de navegación (rutas) */}
        <Navigation />

        {/* Contenedor global de notificaciones Toast */}
        <ToastContainer
          position="bottom-center"
          autoClose={4000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
          theme="light"
        />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;

