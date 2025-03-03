import { useState,useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './HomePage';
import LoginPage from './LoginPage';
import RegisterPage from './RegisterPage';
//const host = "localhost";

function App() {


  return (
    <Router>
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <div style={{ flex: '1 0 auto' }}>
        <Routes>
          <Route path="/" element={<LoginPage />} />
          <Route path="/signup" element={<RegisterPage />} />
          <Route path="/home" element={<HomePage />} />
        
        </Routes>
      </div>
    </div>
  </Router>
  );
  
}

export default App