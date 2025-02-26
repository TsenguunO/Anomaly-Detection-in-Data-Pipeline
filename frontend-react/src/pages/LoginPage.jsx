/* eslint-disable react/no-unescaped-entities */
import { useState } from 'react';

import Container from "react-bootstrap/Container";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

import axios from 'axios'
import { useHistory } from 'react-router-dom';
import { useAuthStore } from "../stores";

function LoginPage() {
  const history = useHistory();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const login = useAuthStore((state) => state.login);
  
  const authenticateUser = async (email, password) => {
    try {

      if (import.meta.env.MODE === 'development') {
        return true;
      }

      const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/Authentication/login`, {
        email,
        password,
      });

      if (!response.status === 200) {
        return false;
      }
      return true;
    } catch (error) {
      return false;
    }
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();

    const isAuthenticated = await authenticateUser(email, password);
    if (isAuthenticated) {
      localStorage.setItem('email', email);
      login(email);
      history.push('/');
    }
  }

  return (
    <div>
      <Container>
      <h1>Login</h1>
      <Form>
      <Form.Group className="mb-3" controlId="formBasicEmail">
        <Form.Label>Email address</Form.Label>
        <Form.Control type="email" placeholder="Enter email" value={email} onChange={(e) => setEmail(e.target.value)}/>
      </Form.Group>

      <Form.Group className="mb-3" controlId="formBasicPassword">
        <Form.Label>Password</Form.Label>
        <Form.Control type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)}/>
      </Form.Group>

      <Button variant="primary" type="submit" onClick={(e) => handleSubmit(e)}>
        Login
      </Button>
    </Form>
      </Container>
    </div>
  );
}

export default LoginPage;