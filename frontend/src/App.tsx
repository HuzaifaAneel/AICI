import React, { useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import ChatPage from './components/ChatPage';

const App: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const verifyToken = async () => {
      const token = localStorage.getItem('token');
      
      if (location.pathname === '/login' || location.pathname === '/register') {
        return;
      }

      if (token) {
        try {
          const response = await axios.get('http://localhost:8080/chat/chat-history', {
            headers: { Authorization: `Bearer ${token}` },
          });

          if (response.status === 200) {
            navigate('/chat');
          }
        } catch (error) {
          console.error('Invalid token:', error);
          localStorage.removeItem('token');
          navigate('/login');
        }
      } else {
        if (location.pathname !== '/login' && location.pathname !== '/register') {
          navigate('/login');
        }
      }
    };

    verifyToken();
  }, [location, navigate]);

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/chat" element={<ChatPage />} />
    </Routes>
  );
};

const MainApp: React.FC = () => (
  <Router>
    <App />
  </Router>
);

export default MainApp;
