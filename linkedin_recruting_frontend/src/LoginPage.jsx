import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
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
      const data = await response.json();
      const result = data.message;

      if (response.ok) {
        sessionStorage.setItem('user', result);
        navigate('/home');
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
    <Box
      sx={{
        backgroundImage: 'url(/aubay.jpg)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        width: '100vw',
        height: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        maxWidth: '100%',
        maxHeight: '100%'
      }}
    >
      <Container maxWidth="sm">
        <Box sx={{ p: 3, border: '1px solid #ddd', borderRadius: 2, boxShadow: 3, bgcolor: 'white', textAlign: 'center' }}>
          <img src="/logo.png" alt="Logo" style={{ width: '150px', marginBottom: '20px' }} />
          <h2 style={{ textAlign: 'center', marginBottom: '20px' }}>Se connecter</h2>
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
          <Button
            variant="contained"
            fullWidth
            onClick={handleLogin}
            sx={{
              background: 'linear-gradient(45deg, #FF0000 30%, #FF6347 90%)',
              color: 'white',
              fontWeight: 'bold',
              '&:hover': {
                background: 'linear-gradient(45deg, #D50000 30%, #FF4500 90%)',
              }
            }}
          >
            Sign-in
          </Button>
          <Box sx={{ mt: 2, textAlign: 'center' }}>
            <a href="/signup" style={{ textDecoration: 'none', color: '#FF0000', fontWeight: 'bold' }}>Sign-up</a>
          </Box>
        </Box>
      </Container>
    </Box>
  );
};

export default LoginPage;
