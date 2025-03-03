import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Button, TextField, Container, Box, Alert } from '@mui/material';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const host = import.meta.env.VITE_HOST;

  


  const handleLogin = async () => {
    try {
      const url = `http://${host}:8081/login/?user=${username}&password=${password}`;
      const response = await fetch(url);

      const data = await response.json(); // Convertir la réponse en JSON
      const result=data.message;
      console.log("------------------------------");
      console.log(result);
      console.log("------------------------------");
      if (response.ok) {

        sessionStorage.setItem('user', result);
        navigate('/home'); // Redirige vers la page d'accueil
        
        
      } else {
        alert(`${result}`);
        console.error("Réponse API :", result);
      }

      
    } catch (err) {
      console.error('Erreur lors de la connexion :', err);
      setError('Erreur de connexion. Veuillez réessayer.');
      alert('Erreur de connexion. Veuillez réessayer.');
    }
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 5 }}>
      <Box sx={{ p: 3, border: '1px solid #ddd', borderRadius: 2 }}>
        <h2>Se connecter</h2>
        {error && <Alert severity="error">{error}</Alert>}
        <TextField
          label="Email"
          fullWidth
          required
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          sx={{ mb: 2 }}
        />
        <TextField
          label="Password"
          type="password"
          fullWidth
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          sx={{ mb: 2 }}
        />
        <Button variant="contained" fullWidth onClick={handleLogin}>
          Sign-in
        </Button>
        <Box sx={{ mt: 2, textAlign: 'center' }}>
          <a href="/signup">Sign-up</a>
        </Box>
      </Box>
    </Container>
  );
};

export default LoginPage;
