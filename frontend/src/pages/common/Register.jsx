// src/pages/common/Register.jsx
// Página de registro de nuevos usuarios escolares.
// Conectada con POST /api/v1/auth/register/ del backend Django.

import { useNavigate, Link } from 'react-router-dom';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { toast } from 'react-toastify';
import { Button, Container, Form, Header, Icon, Message, Segment } from 'semantic-ui-react';
import { registerApi } from '../../api/user';

// Esquema de validación con Yup
const registerSchema = Yup.object({
  email: Yup.string()
    .email('El correo electrónico no tiene un formato válido.')
    .required('El correo electrónico es obligatorio.'),
  password: Yup.string()
    .min(6, 'La contraseña debe tener al menos 6 caracteres.')
    .required('La contraseña es obligatoria.'),
  first_name: Yup.string()
    .required('El nombre es obligatorio.'),
  last_name: Yup.string()
    .required('El apellido es obligatorio.'),
  matricula: Yup.string(),
});

export function Register() {
  const navigate = useNavigate();

  const formik = useFormik({
    initialValues: {
      email: '',
      password: '',
      first_name: '',
      last_name: '',
      matricula: '',
    },
    validationSchema: registerSchema,
    onSubmit: async (values, { setSubmitting }) => {
      try {
        await registerApi(values);
        toast.success('¡Cuenta creada exitosamente! Ya puedes iniciar sesión.');
        navigate('/login');
      } catch (error) {
        toast.error(error.message || 'Error al registrar la cuenta. Intenta de nuevo.');
      } finally {
        setSubmitting(false);
      }
    },
  });

  return (
    <Container className="register-container">
      <Segment padded="very" className="register-segment">
        <Header as="h2" textAlign="center" className="register-header">
          <Icon name="graduation cap" color="teal" />
          <Header.Content>
            CampusConnect
            <Header.Subheader>Crea tu cuenta escolar</Header.Subheader>
          </Header.Content>
        </Header>

        <Form onSubmit={formik.handleSubmit} error noValidate>
          {/* Nombre */}
          <Form.Field error={!!(formik.touched.first_name && formik.errors.first_name)}>
            <label>Nombre</label>
            <Form.Input
              id="first_name"
              name="first_name"
              type="text"
              placeholder="Tu nombre"
              icon="user"
              iconPosition="left"
              value={formik.values.first_name}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
            />
            {formik.touched.first_name && formik.errors.first_name && (
              <Message error content={formik.errors.first_name} />
            )}
          </Form.Field>

          {/* Apellido */}
          <Form.Field error={!!(formik.touched.last_name && formik.errors.last_name)}>
            <label>Apellido</label>
            <Form.Input
              id="last_name"
              name="last_name"
              type="text"
              placeholder="Tu apellido"
              icon="user outline"
              iconPosition="left"
              value={formik.values.last_name}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
            />
            {formik.touched.last_name && formik.errors.last_name && (
              <Message error content={formik.errors.last_name} />
            )}
          </Form.Field>

          {/* Correo Electrónico */}
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

          {/* Matrícula */}
          <Form.Field error={!!(formik.touched.matricula && formik.errors.matricula)}>
            <label>Matrícula (opcional)</label>
            <Form.Input
              id="matricula"
              name="matricula"
              type="text"
              placeholder="MAT-2026-001"
              icon="id card"
              iconPosition="left"
              value={formik.values.matricula}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
            />
            {formik.touched.matricula && formik.errors.matricula && (
              <Message error content={formik.errors.matricula} />
            )}
          </Form.Field>

          {/* Contraseña */}
          <Form.Field error={!!(formik.touched.password && formik.errors.password)}>
            <label>Contraseña</label>
            <Form.Input
              id="password"
              name="password"
              type="password"
              placeholder="Mínimo 6 caracteres"
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

          {/* Botón Registrarse */}
          <Button
            type="submit"
            color="teal"
            fluid
            size="large"
            loading={formik.isSubmitting}
            disabled={formik.isSubmitting}
            className="register-button"
          >
            <Icon name="user plus" />
            Crear Cuenta
          </Button>
        </Form>

        <Message className="register-login-link">
          ¿Ya tienes cuenta?{' '}
          <Link to="/login">Inicia sesión</Link>
        </Message>
      </Segment>
    </Container>
  );
}

