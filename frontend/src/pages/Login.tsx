import React, { useState } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import LoginForm from '../components/LoginForm';
import './Login.css';

const Login: React.FC = () => {
  const { user, isLoading } = useAuth();
  const [isLoginForm, setIsLoginForm] = useState(true);

  if (isLoading) {
    return <div className="loading">Loading...</div>;
  }

  if (user) {
    return <Navigate to="/" replace />;
  }

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-hero">
          <h1>Phishing Awareness LMS</h1>
          <p>Protect yourself and your organization from phishing attacks through comprehensive training and AI-powered assistance.</p>
        </div>
        
        <div className="login-content">
          {isLoginForm ? (
            <LoginForm onSwitchToRegister={() => setIsLoginForm(false)} />
          ) : (
            <div className="register-placeholder">
              <h2>Registration</h2>
              <p>Please contact your administrator to create an account.</p>
              <button 
                onClick={() => setIsLoginForm(true)}
                className="switch-btn"
              >
                Back to Login
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Login;