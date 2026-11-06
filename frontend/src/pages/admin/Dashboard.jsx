// src/pages/admin/Dashboard.jsx
// Pantalla del Dashboard del administrador/usuario autenticado.
// Muestra el correo del usuario y un botón para cerrar sesión.

import { Button, Container, Header, Segment, Icon } from 'semantic-ui-react';
import { useAuth } from '../../hooks/useAuth';
import { useNavigate } from 'react-router-dom';

export function Dashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <Container className="dashboard-container">
      <Segment padded="very" className="dashboard-segment">
        <Header as="h1" textAlign="center" className="dashboard-title">
          <Icon name="graduation cap" />
          <Header.Content>
            Dashboard
            <Header.Subheader>Plataforma Escolar CampusConnect</Header.Subheader>
          </Header.Content>
        </Header>

        <Segment basic textAlign="center">
          <Header as="h3" color="grey">
            <Icon name="user circle" />
            Bienvenido/a
          </Header>
          <p className="dashboard-email">
            <strong>{user?.email}</strong>
          </p>
          {user?.first_name && (
            <p className="dashboard-name">
              {user.first_name} {user.last_name}
            </p>
          )}
          {user?.matricula && (
            <p className="dashboard-matricula">
              Matrícula: <strong>{user.matricula}</strong>
            </p>
          )}
        </Segment>

        <Segment basic textAlign="center">
          <Button
            color="red"
            icon
            labelPosition="left"
            onClick={handleLogout}
            className="logout-button"
          >
            <Icon name="sign out" />
            Cerrar Sesión
          </Button>
        </Segment>
      </Segment>
    </Container>
  );
}

