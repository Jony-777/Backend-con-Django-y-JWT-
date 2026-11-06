// src/pages/common/Error404.jsx
// Página mostrada cuando la ruta no existe.

import { Container, Header, Icon, Button, Segment } from 'semantic-ui-react';
import { Link } from 'react-router-dom';

export function Error404() {
  return (
    <Container textAlign="center" className="error404-container">
      <Segment padded="very" basic>
        <Icon name="warning sign" size="massive" color="yellow" />
        <Header as="h1" className="error404-title">
          404 - Página no encontrada
        </Header>
        <p>La página que buscas no existe o ha sido movida.</p>
        <Button as={Link} to="/" color="teal" icon labelPosition="left">
          <Icon name="home" />
          Volver al inicio
        </Button>
      </Segment>
    </Container>
  );
}

