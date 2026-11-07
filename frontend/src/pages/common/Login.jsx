// src/pages/common/Login.jsx
// Página de inicio de sesión con Formik + Yup + Semantic UI + React Toastify.

import { useNavigate, Link } from 'react-router-dom';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { toast } from 'react-toastify';
import { Button, Container, Form, Header, Icon, Message, Segment } from 'semantic-ui-react';
import { loginApi } from '../../api/user';
import { useAuth } from '../../hooks/useAuth';

// Esquema de validación con Yup
const loginSchema = Yup.object({
  email: Yup.string()
    .email('El correo electrónico no tiene un formato válido.')
    .required('El correo electrónico es obligatorio.'),
  password: Yup.string()
    .required('La contraseña es obligatoria.'),
});

export function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const formik = useFormik({
    initialValues: { email: '', password: '' },
    validationSchema: loginSchema,
    onSubmit: async (values, { setSubmitting }) => {
      try {
        // 1. Llamar al endpoint POST /api/v1/auth/token/
        const data = await loginApi(values.email, values.password);

        // 2. Guardar el token y recuperar los datos del usuario vía AuthContext
        await login(data.access);

        // 3. Redirigir al Dashboard
        navigate('/dashboard');
      } catch (error) {
        // Mostrar notificación de error con React Toastify
        toast.error(error.message || 'Error al iniciar sesión. Verifica tus credenciales.');
      } finally {
        setSubmitting(false);
      }
    },
  });

  return (
    <Container className="login-container">
      <Segment padded="very" className="login-segment">
        <Header as="h2" textAlign="center" className="login-header">
          <Icon name="graduation cap" color="teal" />
          <Header.Content>
            CampusTrack
            <Header.Subheader>Inicia sesión en tu cuenta</Header.Subheader>
          </Header.Content>
        </Header>

        <Form onSubmit={formik.handleSubmit} error noValidate>
          {/* Campo de Correo Electrónico */}
          <Form.Field error={!!(formik.touched.email && formik.errors.email)}>
            <label>Correo Electrónico</label>
            <Form.Input
              id="email"
              name="email"
              type="email"
              placeholder="correo@ejemplo.com"
              icon="mail"
              iconPosition="left"
              value={formik.values.email}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
            />
            {formik.touched.email && formik.errors.email && (
              <Message error content={formik.errors.email} />
            )}
          </Form.Field>

          {/* Campo de Contraseña */}
          <Form.Field error={!!(formik.touched.password && formik.errors.password)}>
            <label>Contraseña</label>
            <Form.Input
              id="password"
              name="password"
              type="password"
              placeholder="Tu contraseña"
              icon="lock"
              iconPosition="left"
              value={formik.values.password}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
            />
            {formik.touched.password && formik.errors.password && (
              <Message error content={formik.errors.password} />
            )}
          </Form.Field>

          {/* Botón de Login */}
          <Button
            type="submit"
            color="teal"
            fluid
            size="large"
            loading={formik.isSubmitting}
            disabled={formik.isSubmitting}
            className="login-button"
          >
            <Icon name="sign in" />
            Iniciar Sesión
          </Button>
        </Form>

        <Message className="login-register-link">
          ¿No tienes cuenta?{' '}
          <Link to="/register">Regístrate aquí</Link>
        </Message>
      </Segment>
    </Container>
  );
}

