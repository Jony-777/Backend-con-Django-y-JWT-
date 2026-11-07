// src/pages/client/Home.jsx
// Página de inicio pública de CampusConnect.

import { Container, Header, Icon, Segment } from 'semantic-ui-react';

export function Home() {
  return (
    <Container className="home-container">
      <Segment padded="very" basic textAlign="center" className="home-segment">
        <Icon name="graduation cap" size="huge" color="teal" />
        <Header as="h1" color="teal">
          CampusTrack
        </Header>
        <Header.Subheader as="p" className="home-subtitle">
          Plataforma Escolar de Gestión de Usuarios
        </Header.Subheader>
        <p>Bienvenido a la plataforma. Inicia sesión para acceder a tu Dashboard.</p>
      </Segment>
    </Container>
  );
}

