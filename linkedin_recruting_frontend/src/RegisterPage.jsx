import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Button, TextField, Container, Box, Alert } from '@mui/material';

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
  });
  const [success, setSuccess] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const host = import.meta.env.VITE_HOST;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSignUp = async () => {
    try {

      const response = await axios.post(`http://${host}:8081/register/`, formData);


      console.log('Status:', response.status);

      console.log("------------------------------");
     
      if (response.status === 200) {
        console.log("'Account created successfully! You can log in.")
        setSuccess('Account created successfully! You can log in.');
        
        alert('Account created successfully! You can log in.');
        navigate('/')
        
      }

    } catch (err) {
      console.error('Erreur lors de la création du compte :', err);
      setError('Error creating account. Please try again.');
      alert(error)
      alert(err)
    }
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 5 }}>
      <Box sx={{ p: 3, border: '1px solid #ddd', borderRadius: 2 }}>
        <h2>Créer un compte</h2>
        {success && <Alert severity="success">{success}</Alert>}
        {error && <Alert severity="error">{error}</Alert>}
        <TextField
          label="Formal Name"
          name="username"
          fullWidth
          required
          value={formData.username}
          onChange={handleChange}
          sx={{ mb: 2 }}
        />
       
        <TextField
          label="Email"
          name="email"
          type="email"
          fullWidth
          required
          value={formData.email}
          onChange={handleChange}
          sx={{ mb: 2 }}
        />
        <TextField
          label="Mot de passe"
          name="password"
          type="password"
          fullWidth
          required
          value={formData.password}
          onChange={handleChange}
          sx={{ mb: 2 }}
        />
        
        <Button variant="contained" fullWidth onClick={handleSignUp}>
          S'inscrire
        </Button>
        <Box sx={{ mt: 2, textAlign: 'center' }}>
          <a href="/">Se connecter</a>
        </Box>
      </Box>
    </Container>
  );
};

export default RegisterPage;