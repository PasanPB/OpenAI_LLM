import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Navbar.css';

const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const location = useLocation();

  const handleLogout = () => {
    logout();
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          Phishing Awareness LMS
        </Link>
        
        <div className="navbar-menu">
          {user ? (
            <>
              <Link 
                to="/" 
                className={`navbar-item ${location.pathname === '/' ? 'active' : ''}`}
              >
                Dashboard
              </Link>
              <Link 
                to="/exam" 
                className={`navbar-item ${location.pathname === '/exam' ? 'active' : ''}`}
              >
                Exam
              </Link>
              <Link 
                to="/training" 
                className={`navbar-item ${location.pathname === '/training' ? 'active' : ''}`}
              >
                Training
              </Link>
              <Link 
                to="/chatbot" 
                className={`navbar-item ${location.pathname === '/chatbot' ? 'active' : ''}`}
              >
                AI Assistant
              </Link>
              
              <div className="navbar-user">
                <span className="user-name">{user.name}</span>
                <span className={`user-level ${user.classification}`}>
                  {user.classification}
                </span>
                <button onClick={handleLogout} className="logout-btn">
                  Logout
                </button>
              </div>
            </>
          ) : (
            <Link to="/login" className="navbar-item">
              Login
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;