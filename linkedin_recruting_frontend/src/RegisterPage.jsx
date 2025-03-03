import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Button, TextField, Container, Box, Alert, LinearProgress, Typography } from '@mui/material';

// Fonction pour évaluer la force du mot de passe
const evaluatePasswordStrength = (password) => {
  const regexLower = /[a-z]/;
  const regexUpper = /[A-Z]/;
  const regexDigit = /\d/;
  const regexSpecial = /[!@#$%^&*(),.?":{}|<>]/;
  
  let strength = 0;
  if (regexLower.test(password)) strength++;
  if (regexUpper.test(password)) strength++;
  if (regexDigit.test(password)) strength++;
  if (regexSpecial.test(password)) strength++;
  if (password.length >= 8) strength++;

  if (strength <= 1) return 'Very Weak';
  if (strength === 2) return 'Weak';
  if (strength === 3) return 'Medium';
  if (strength === 4) return 'Strong';
  return 'Very Strong';
};

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
  });
  const [success, setSuccess] = useState(null);
  const [error, setError] = useState(null);
  const [passwordStrength, setPasswordStrength] = useState('');
  const navigate = useNavigate();
  const host = import.meta.env.VITE_HOST;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));

    if (name === 'password') {
      setPasswordStrength(evaluatePasswordStrength(value));
    }
  };

  const validateEmail = (email) => {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@aubay\.com$/;
    return emailRegex.test(email) && email.length >= 8;
  };

  const validatePassword = (password) => {
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$/;
    return passwordRegex.test(password);
  };

  const handleSignUp = async () => {
    if (!validateEmail(formData.email)) {
      setError('Email must be in the format xxx@aubay.com and at least 8 characters long.');
      return;
    }

    if (!validatePassword(formData.password)) {
      setError('Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character.');
      return;
    }

    try {
      const response = await axios.post(`http://${host}:8081/register/`, formData);

      if (response.status === 200) {
        setSuccess('Account created successfully! You can log in.');
        alert('Account created successfully! You can log in.');
        navigate('/');
      }
    } catch (err) {
      setError('Error creating account. Please try again.');
      alert(err);
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
        overflow: 'hidden',
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        maxWidth: '100%',
        maxHeight: '100%',
        overflowX: 'hidden',
        overflowY: 'hidden',
      }}
    >
      <Container maxWidth="sm" sx={{ mt: 5 }}>
        <Box sx={{ p: 3, border: '1px solid #ddd', borderRadius: 2, boxShadow: 3, bgcolor: 'white', textAlign: 'center' }}>
          <img src="/logo.png" alt="Logo" style={{ width: '150px', marginBottom: '20px' }} />
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
            error={!validateEmail(formData.email)}
            helperText={!validateEmail(formData.email) ? 'Email must be in the format xxx@aubay.com and at least 8 characters long.' : ''}
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
            error={!validatePassword(formData.password)}
            helperText={!validatePassword(formData.password) ? 'Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character.' : ''}
          />
          <Typography variant="body2" color="textSecondary">
            Password Strength: {passwordStrength}
          </Typography>
          <LinearProgress
            variant="determinate"
            value={passwordStrength === 'Weak' ? 25 : passwordStrength === 'Medium' ? 50 : passwordStrength === 'Strong' ? 75 : 100}
            sx={{ mb: 2 }}
          />
          <Button
            variant="contained"
            fullWidth
            onClick={handleSignUp}
            sx={{
              background: 'linear-gradient(45deg, #FF0000 30%, #FF6347 90%)',
              color: 'white',
              fontWeight: 'bold',
              '&:hover': {
                background: 'linear-gradient(45deg, #D50000 30%, #FF4500 90%)',
              },
            }}
          >
            Sign Up
          </Button>
          <br />
          you have an account?
          <br />
          <Box sx={{ mt: 2, textAlign: 'center' }}>
            <a href="/" style={{ textDecoration: 'none', color: '#FF0000', fontWeight: 'bold' }}>Sign In</a>
          </Box>
        </Box>
      </Container>
    </Box>
  );
};

export default RegisterPage;
